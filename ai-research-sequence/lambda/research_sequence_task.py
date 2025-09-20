# from dotenv import load_dotenv
import os
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
# from openai import OpenAI
from exa_py import Exa
from prompt_factory import PromptFactory  # ⬅️ ADD THIS IMPORT
import requests

class ResearchSequenceTask:
    """
    A class to handle the full workflow of clarifying questions, formula brainstorming,
    data sourcing via Exa, and result synthesis for market sizing tasks, using PromptFactory.
    """

    def __init__(self, exa_client=None, openai_client=None):
        # load_dotenv()
        self.EXA_API_KEY = os.getenv("EXA_API_KEY")
        self.api_key = os.getenv("OPENAI_API_KEY")
        # self.client = openai_client or OpenAI()
        self.exa = exa_client or Exa(self.EXA_API_KEY)
        self.system_message = (
            "You are a professional market sizing assistant. "
            "Your role is to design clear, structured models for market sizing problems, "
            "identify and list the key data inputs needed, and suggest possible data sources or proxies "
            "when direct data is unavailable. Always present your answers in a structured deconstructed format."
        )


    # def chat_response_package(self, prompt, response_json=False):
    #     """
    #     Calls OpenAI with the given prompt.
    #     Returns JSON if response_json=True, otherwise returns text.
    #     """
    #     response = self.client.chat.completions.create(
    #         model="gpt-4o",
    #         messages=[
    #             {"role": "system", "content": self.system_message},
    #             {"role": "user", "content": prompt}
    #         ],
    #         response_format={"type": "json_object"} if response_json else None
    #     )
    #     return response.choices[0].message.content

    def chat_response(self, prompt, response_json=False):
        """
        Calls OpenAI endpoint with the given prompt.
        Returns JSON if response_json=True, otherwise returns text.
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt}
            ],
        }
        # Add response format if JSON requested
        if response_json:
            data["response_format"] = {"type": "json_object"}

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise error for bad status codes

        result = response.json()
        return result["choices"][0]["message"]["content"]


    def get_clarifying_questions(self, market_description):
        """
        Generates clarifying questions for the given market description using PromptFactory.
        """
        prompt = PromptFactory.get_prompt(
            "clarifying_questions_prompt",
            market_description=market_description
        )
        return self.chat_response(prompt)

    def generate_market_formulas(self, market_description):
        """
        Runs brainstorm prompt and extracts formulas from the response using PromptFactory.
        """
        prompt = PromptFactory.get_prompt(
            "formula_brainstorm_prompt",
            market_description=market_description
        )
        response = self.chat_response(prompt, response_json=True)
        data = json.loads(response)
        return data.get("formula", [])

    def find_data_for_formula(self, formula):
        """
        Finds potential data sources for the given formula using PromptFactory.
        """
        prompt = PromptFactory.get_prompt(
            "datasource_prompt",
            formula=formula
        )
        response = self.chat_response(prompt, response_json=True)
        return json.loads(response)

    def get_components_from_formula(self, formula: str) -> list:
        """
        Decomposes a formula string into individual components using the language model.
        Returns a list of component names.
        """
        prompt = PromptFactory.get_prompt(
            "decompose_formula_prompt",
            formula=formula
        )
        response = self.chat_response(prompt, response_json=True)
        data = json.loads(response)
        components = data.get("components", [])

        if not isinstance(components, list):
            print(f"[WARNING] Unexpected components format in response: {components}")
            return []

        return components

    def exa_search(self, query):
        """
        Runs an Exa semantic search query.
        """
        return self.exa.answer(query, stream=False, text=True)

    def exa_data_extraction(self, exa_answer_result, component):
        """
        Extracts numeric data points from Exa answers and synthesizes them via OpenAI using PromptFactory.
        """
        mapping = {
            "title": "DATA_SOURCE_NAME",
            "url": "DATA_SOURCE_LINK",
            "text": "DATA_SOURCE_TEXT",
        }
        data_source = {
            output_key: getattr(exa_answer_result, input_attr, None)
            for input_attr, output_key in mapping.items()
        }

        exa_synthesis_prompt = PromptFactory.get_prompt(
            "exa_synthesis_prompt",
            text=data_source.get("DATA_SOURCE_TEXT", ""),
            component=component
        )

        synthesis_response = self.chat_response(exa_synthesis_prompt, response_json=True)
        synthesis_json = json.loads(synthesis_response)
        return {'component': component} | data_source | synthesis_json

    def parallel_exa_extraction(self, exa_results, component):
        """
        Runs exa_data_extraction in parallel over a list of Exa citations.
        Returns a list of merged results.
        """
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.exa_data_extraction, result, component)
                for result in exa_results
            ]
            for future in as_completed(futures):
                results.append(future.result())
        return results

    def run_exa_workflow(self, query: str, component: str) -> list:
        """
        Executes the full Exa data sourcing workflow.
        """
        print(f"[INFO] Running Exa semantic search for query: {query}")
        exa_result = self.exa_search(query)
        print(f"[INFO] Retrieved {len(exa_result.citations)} citations from Exa.")

        print("[INFO] Starting parallel extraction of data points from Exa citations...")
        results = self.parallel_exa_extraction(exa_result.citations, component)
        print("[INFO] Extraction complete. Returning DataFrame.")

        return results

    def run_exa_workflow_for_components_sequential(self, components: list) -> dict:
        """
        Executes the Exa data sourcing workflow for each component sequentially.
        """
        all_results = {}
        print(f"[INFO] Components: {components}")

        for component in components:
            print(f"\n[INFO] Processing component: '{component}' sequentially")
            try:
                df = self.run_exa_workflow(query=component, component=component)
                all_results[component] = df
                print(f"[INFO] Completed workflow for component: '{component}'")
            except Exception as e:
                print(f"[ERROR] Failed workflow for component '{component}': {e}")
                all_results[component] = None

        print("[INFO] Exa workflows complete for all components (sequential execution).")
        return all_results
