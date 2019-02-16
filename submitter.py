import re
import sys

import requests

# Last update: 2019-02-16
lang_choice = {
    "C++14": 88,
    "Java": 3,
    "Python 3": 28,
    "C11": 75,
    "PyPy3": 73,
    "C": 0,
    "C++": 1,
    "C++11": 49,
    "C++17": 84,
    "Java (OpenJDK)": 91,
    "Java 11": 93,
    "Python 2": 6,
    "PyPy2": 32,
    "Ruby 2.5": 68,
    "Kotlin (JVM)": 69,
    "Kotlin (Native)": 92,
    "Swift": 74,
    "Text": 58,
    "C# 6.0": 62,
    "node.js": 17,
    "Go": 12,
    "D": 29,
    "F#": 37,
    "PHP": 7,
    "Rust": 44,
    "Pascal": 2,
    "Lua": 16,
    "Perl": 8,
    "R": 72,
    "Objective-C": 10,
    "Objective-C++": 64,
    "C (Clang)": 59,
    "C++ (Clang)": 60,
    "C++11 (Clang)": 66,
    "C++14 (Clang)": 67,
    "C11 (Clang)": 77,
    "C++17 (Clang)": 85,
    "Golfscript": 79,
    "Assembly (32bit)": 27,
    "Assembly (64bit)": 87,
    "VB.NET 4.0": 63,
    "Bash": 5,
    "Fortran": 13,
    "Scheme": 14,
    "Ada": 19,
    "awk": 21,
    "OCaml": 22,
    "Brainfuck": 23,
    "Whitespace": 24,
    "Tcl": 26,
    "Rhino": 34,
    "Cobol": 35,
    "Pike": 41,
    "sed": 43,
    "Boo": 46,
    "Intercal": 47,
    "bc": 48,
    "Nemerle": 53,
    "Cobra": 54,
    "Algol 68": 70,
    "Befunge": 71,
    "Haxe": 81,
    "LOLCODE": 82,
    "아희": 83,
}

# HTTP response code
resp = {
    200: "OK",
    400: "Bad request",
    403: "Forbidden",
    404: "Not found",
    500: "Internal server error"
}

if __name__ == "__main__":
    # Zero or two command line arguments are accepted
    assert len(sys.argv)==1 or len(sys.argv)==3, "Specify the language and source location (in this order). Provide both, or none."
    
    # Strat new session
    s = requests.session()

    # Fetch credentials from pass.txt and perform login
    with open('pass.txt', 'r') as f:
        username = f.readline().strip()
        password = f.readline().strip()
        
        data = {
            'login_user_id': username,
            'login_password': password,
            'next': '/'
        }
        login_response = s.post('https://www.acmicpc.net/signin', data)
        
        # Analyze response
        resp_code = login_response.status_code
        print(f'Login: response {resp_code} {resp.get(resp_code, "")}')
        if login_response.text.find('잘못되었습니다')!=-1:
            print('Login failed. Wrong username or password!')
            quit()

    # Fetch problem number from sample.txt
    with open('sample.txt', 'r') as f:
        prob_id = re.findall(r'icpc.me/(\d+)\n', f.read())[0]
    
    # Find csrf_key value
    submit_url = 'https://www.acmicpc.net/submit/' + prob_id
    r = s.get(submit_url)
    idx = r.text.find('csrf_key')
    csrf_key = r.text[idx+17:idx+49]

    # Set language and code confidentiality
    language = lang_choice[sys.argv[1] if len(sys.argv)>1 else 'Python 3']
    code_open = 'open'  # 'open', 'close', 'onlyaccepted'
    
    # Read source code from PATH specified in PATH
    if len(sys.argv)>2:
        PATH = sys.argv[2]
    else:
        PATH = 'main.py'
    with open(PATH,'r') as f:
        source = f.read()
    
    # Fill in request data
    data = {
        'problem_id': prob_id,
        'language': language,
        'code_open': code_open,
        'source': source,
        'csrf_key': csrf_key
    }
    
    # Submit and print response
    submit_response = s.post(submit_url, data=data)
    resp_code = submit_response.status_code
    print(f'Submit: response {resp_code} {resp.get(resp_code, "")}')
