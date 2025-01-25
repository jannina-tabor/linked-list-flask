import logging
from flask import Flask, render_template, request, flash
from LinkedList import LinkedList

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

linked_list = LinkedList()

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html', linked_list=linked_list.print_list())

@app.route('/update', methods=['POST'])
def update():
    print("POST request received at /update")  # Add this for debugging
   
    operation = request.form.get('operation')
    data = request.form.get('data')
    
    logging.debug(f"Received operation: {operation}")
    logging.debug(f"Received data: {data}")
    
    if not operation:
        flash ('No operation provided', 'error')
        return render_template('index.html', linked_list=linked_list.print_list())
    
    # Validate the data when required
    if operation in ["insert_beginning", "insert_end", "remove_at"] and not data:
        flash ('Please provide data for the operation', 'error')
        return render_template('index.html', linked_list=linked_list.print_list())

    try:
        # Operations based on the button clicked
        if operation == "insert_beginning" and data:
            linked_list.insert_at_beginning(data)
            flash(f'Inserted {data} at the beginning.', 'success')
        elif operation == "insert_end" and data:
            linked_list.insert_at_end(data)
            flash(f'Inserted {data} at the end.', 'success')
        elif operation == "remove_beginning":
            if linked_list.head:  # If the list isn't empty
                removed_data = linked_list.remove_beginning()
                flash(f"Removed '{removed_data}' from the beginning.", 'success')
            else:
                flash("The list is empty. No element to remove.", 'error')
        elif operation == "remove_end":
            if linked_list.head:  # If the list isn't empty
                removed_data = linked_list.remove_end()
                flash(f"Removed '{removed_data}' from the end.", 'success')
            else:
                flash("The list is empty. No element to remove.", 'error')
        elif operation == "remove_at" and data:
            found = linked_list.search(data)
            if found:
                linked_list.remove_at(data)
                flash(f"Removed '{data}' from the list.", 'success')
            else:
                flash(f"Data '{data}' not found in the list.", 'error')
        elif operation == "search":
            found = linked_list.search(data)
            flash(f"Data '{data}' found in the list." if found else f"Data '{data}' not found in the list.", 'info')
        else:
            flash('Invalid operation.', 'error')
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")  # Log error for debugging
        flash(f"An error occurred: {str(e)}", 'error')
        
    return render_template('index.html', linked_list=linked_list.print_list())

if __name__ == "__main__":
    app.run(debug=True)
