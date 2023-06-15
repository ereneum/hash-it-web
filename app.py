from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    output = None

    if request.method == 'POST':
        user_input = request.form['user_input']
        first_digits = request.form['first_digits']
        last_digits = request.form['last_digits']
        last_first = request.form.get('last_first')

        if not user_input:
            error = "Enter a valid input."
        else:
            try:
                first_digits = int(first_digits)
                last_digits = int(last_digits)

                # Compute SHA-256 hash
                hash_object = hashlib.sha256(user_input.encode())
                hashed_version = hash_object.hexdigest()

                # Generate desired output format
                first_digits_str = hashed_version[:first_digits]
                last_digits_str = hashed_version[-last_digits:]

                if last_first:
                    output = last_digits_str + "!" + first_digits_str
                else:
                    output = first_digits_str + "!" + last_digits_str

                for i in range(len(output)):
                    if output[i].isnumeric():
                        continue
                    output = output[:i] + output[i].upper() + output[i+1:]
                    break

            except ValueError:
                error = "Enter a valid input."

    return render_template('index.html', output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
