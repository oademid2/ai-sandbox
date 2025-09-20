class PromptFactory:
    """
    Factory class with standardized prompts for market sizing tasks.
    Prompts can be retrieved by calling `get_prompt(prompt_name, **kwargs)`,
    where prompt_name must exactly match one of the defined static method names.
    """

    @staticmethod
    def clarifying_questions_prompt(market_description: str) -> str:
        return (
            f"I want to size the market for: {market_description}.\n\n"
            "Before generating the formula, are there any clarifying questions to get additional context needed for a good formula?\n\n"
            "These questions should directly inform the formula inputs."
        )

    @staticmethod
    def formula_brainstorm_prompt(market_description: str) -> str:
        return (
            f"I want to size the market for: {market_description}.\n\n"
            "Please return a JSON with the following fields:\n\n"
            "steps: string - A numbered overview of the steps.\n"
            "formula: list of strings - Market sizing formulas expressed as strings, excluding explicit adoption/penetration rates.\n"
            "clarifications: list of strings - Clarifying questions to consider for the formulas."
        )

    @staticmethod
    def datasource_prompt(formula: str) -> str:
        return (
            f"This is the formula which I want to apply for market modeling:\n\n{formula}\n\n"
            "Create a JSON of all the components of the formula.\n\n"
            "For each component, find different sources that can be used to find the data point.\n\n"
            "Please return a JSON with the following fields:\n\n"
            "components: list of component_data objects\n"
            "component_data objects:\n"
            "  -- component: name of component\n"
            "  -- data_sources: list of data source objects with fields:\n"
            "       -- DATA_COMPONENT: component name\n"
            "       -- DATA_SOURCE_NAME: name of data source\n"
            "       -- DATA_SOURCE_LINK: link to data source\n"
            "       -- DATA_SOURCE_OVERVIEW: text description/preview of data source\n"
            "       -- DATA_POINT: numeric data value for the component"
        )

    @staticmethod
    def exa_synthesis_prompt(text: str, component: str) -> str:
        return (
            f"The following text is from a data source:\n{text}\n\n"
            f"Please extract a numeric data point for {component}.\n"
            "Then provide a short summary of the text as condensed as possible.\n\n"
            "Please return the response in JSON format with the following structure:\n\n"
            "DATA_POINT: numeric data point for the component\n"
            "DATA_SOURCE_OVERVIEW: a short summary of the text, providing an overview of the information contained in the text."
        )

    @staticmethod
    def decompose_formula_prompt(formula: str) -> str:
        return (
            f"I have a market size formula: {formula}\n\n"
            "Decompose the formula into each individual component / data.\n\n"
            "Return this as a JSON with the following fields:\n\n"
            "components : list of strings, each string is the name of a component."
        )

    @classmethod
    def get_prompt(cls, name: str, **kwargs) -> str:
        """
        Routes a prompt name to the appropriate prompt generator.
        Keys must match the exact function names.
        """
        router = {
            "clarifying_questions_prompt": cls.clarifying_questions_prompt,
            "formula_brainstorm_prompt": cls.formula_brainstorm_prompt,
            "datasource_prompt": cls.datasource_prompt,
            "exa_synthesis_prompt": cls.exa_synthesis_prompt,
            "decompose_formula_prompt": cls.decompose_formula_prompt,
        }

        if name not in router:
            raise ValueError(
                f"Unknown prompt name '{name}'. Valid options: {list(router.keys())}"
            )

        return router[name](**kwargs)
