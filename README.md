# Enigma Machine

This project simulates the operation of an Enigma machine, allowing users to encrypt or decrypt messages through a web interface.

## Getting Started

### Prerequisites

- Python 3.9+
- Uvicorn (for running the application)

### Installation

1. Clone this repository to your local machine:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the application using Uvicorn:
```bash
uvicorn app:app --reload
```

Visit the application in your web browser at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Application Workflow

### 1. Home Page

When you visit the home page, you will find instructions on how to set up the Enigma machine.

From here, click the **"Go to Action Page"** button to proceed to the next page.

### 2. Action Page

On the Action Page, you will see a JSON field pre-filled with an example configuration:

```json
{
    "message": "hello",
    "r1": 0,
    "r2": 0,
    "r3": 0,
    "plugboard": "A:A / C:C / E:E"
}
```

#### Customizing the Configuration

- **Message**: Enter the text you want to encrypt or decrypt in the `message` field.
- **Rotors**: Adjust the `r1`, `r2`, `r3`, `r4` and `r5` (only 3 at a time) fields to change the rotor positions.
- **Plugboard Settings**: Modify the `plugboard` field to specify letter pairings for substitution (e.g., `A:B / C:D`).

#### Submitting the Configuration

1. After configuring the settings and adding your message, click the **Send** button.
2. The application will process the input and display the encrypted or decrypted message on the next page.

### 3. Result Page

On the Result Page, you will see the output of your configuration:
- The encrypted or decrypted message.

Click the **Back to Configuration** button to return to the home.

## Features

- Customize rotors and their initial positions.
- Configure the plugboard for letter substitution.
- Encrypt or decrypt messages based on the Enigma machine's configuration.

## Example Usage

1. Start the app with:
   ```bash
   uvicorn app:app --reload
   ```
2. Visit the home page at [http://127.0.0.1:8000](http://127.0.0.1:8000).
3. Follow the instructions to set up the machine.
4. Go to the Action Page and modify the JSON fields to customize your encryption/decryption settings.
5. Click **Send** to see the result.
6. Use **Back to Configuration** to return to the home page.


