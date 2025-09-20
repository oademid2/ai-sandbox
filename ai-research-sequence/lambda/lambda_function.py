import json
from research_sequence_task import ResearchSequenceTask

task = ResearchSequenceTask()

def lambda_handler(event, context):
    # Add comprehensive debug logging
    print("DEBUG: Full event =", json.dumps(event, indent=2))
    print("DEBUG: httpMethod =", event.get("httpMethod"))
    print("DEBUG: body type =", type(event.get("body")))
    print("DEBUG: body content =", event.get("body"))
    print("DEBUG: queryStringParameters =", event.get("queryStringParameters"))
    
    # Handle CORS preflight requests
    if event.get("httpMethod") == "OPTIONS":
        return _response(200, {"message": "OK"})

    params = event.get("queryStringParameters") or {}
    print("DEBUG: params =", params)

    action = params.get("action")
    if not action:
        return _response(400, {"error": "Missing required query parameter: action"})

    print("DEBUG: action =", action)

    if action == "brainstorm":
        market_description = params.get("market_description")
        if not market_description:
            return _response(400, {"error": "Missing 'market_description' for brainstorm action"})
        formulas = task.generate_market_formulas(market_description)
        return _response(200, {"formulas": formulas})

    elif action == "decompose":
        formula = params.get("formula")
        if not formula:
            return _response(400, {"error": "Missing 'formula' for decompose action"})
        components = task.get_components_from_formula(formula)
        return _response(200, {"components": components})

    elif action == "datasource":
        print("DEBUG: Processing datasource action")
        print("DEBUG: event body =", event.get("body"))
        print("DEBUG: event body type =", type(event.get("body")))
        
        try:
            body = json.loads(event.get("body") or "{}")
            print("DEBUG: parsed body =", body)
        except json.JSONDecodeError as e:
            print("DEBUG: JSON decode error =", e)
            return _response(400, {"error": "Invalid JSON in request body"})

        components = body.get("components")
        print("DEBUG: components type =", type(components))
        print("DEBUG: components =", components)
        
        if not isinstance(components, list):
            return _response(400, {"error": "'components' must be a list in the request body"})

        datasources = task.run_exa_workflow_for_components_sequential(components)
        return _response(200, {"datasources": datasources})

    else:
        return _response(400, {"error": f"Unknown action: {action}"})


def _response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(body_dict)
    }
