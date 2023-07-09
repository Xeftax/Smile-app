# Prerequisite

* You must have Python 3 installed.

* Open a Terminal (Linux and macOS) or Command Prompt (Windows).

* Know the Python command. It can be "`python`", "`python3`", or "`py`". You can check by executing "`python --version`", "`python3 --version`", or "`py --version`".

# Build (with a virtual venv)

* Create an environment:
    ```
    python -m venv venv
    ```

* Activate the environment (Linux and macOS):
    ```
    source venv/bin/activate
    ```

* Activate the environment (Windows):
    ```
    venv\Scripts\activate.ps1
    ```

    <div style="background-color: #f0f8ff; padding: 10px; margin-top: 20px; border-radius: 5px;">
    <strong>Note:</strong> 
    '(venv)' will appear in the header of the command line.
    </div>

    <div style="background-color: #ffdbdb; padding: 10px; margin-top: 20px; margin-bottom: 15px; border-radius: 5px;">
    <strong>Error:</strong> If you have an error because script execution is disabled, you can try this:
        <div style="background-color: #ffffff; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
        Get-ExecutionPolicy
        </div>
    If the current policy is set to 'Restricted', update it to 'RemoteSigned':
        <div style="background-color: #ffffff; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
        Set-ExecutionPolicy RemoteSigned
        </div>

    <https://learn.microsoft.com/fr-fr/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.3>
    </div>

* Install all requirements:
    ```
		pip install -r requirements.txt
    ```

    <div style="background-color: #f0f8ff; padding: 10px; margin-top: 20px; border-radius: 5px;">
    <strong>Note:</strong> 
    If 'pip' is not recognized, you can write 'python -m pip' instead.
    </div>


# Run

* Execute the `main.py` file in the virtual environment:
    ```
    python main.py
    ```

# Troubleshooting

* If you encounter this error in Windows:

    ```
    ImportError: DLL load failed while importing _framework_bindings: %1
    ```

	Install the latest C++ Microsoft Library: <https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170>

