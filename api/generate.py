from http.server import BaseHTTPRequestHandler
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import zipfile
import os

tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-mono")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-mono")

def generate_code(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"],
        max_length=200,  # Small size to work fast
        do_sample=True,
        top_p=0.95,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def handler(event, context):
    if event["httpMethod"] != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    body = json.loads(event["body"])
    app_description = body.get("description", "")

    backend_prompt = f"Create a Flask API for {app_description}"
    frontend_prompt = f"Create a React app for {app_description}"
    
    backend_code = generate_code(backend_prompt)
    frontend_code = generate_code(frontend_prompt)

    with open("/tmp/backend.py", "w") as f:
        f.write(backend_code)
    with open("/tmp/frontend.js", "w") as f:
        f.write(frontend_code)

    zip_path = "/tmp/generated_app.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write("/tmp/backend.py", "backend.py")
        zipf.write("/tmp/frontend.js", "frontend.js")

    with open(zip_path, "rb") as f:
        zip_content = f.read()

    os.remove("/tmp/backend.py")
    os.remove("/tmp/frontend.js")
    os.remove(zip_path)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/zip",
            "Content-Disposition": "attachment; filename=generated_app.zip"
        },
        "body": zip_content.hex(),
        "isBase64Encoded": True
    }