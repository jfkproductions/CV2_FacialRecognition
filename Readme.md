
## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    python app.py
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000`.
2. Upload an image to detect faces.
3. View the results on the result page.

## Dependencies

- Flask
- OpenCV
- NumPy

## License

This project is licensed under the MIT License. See the LICENSE file for details.