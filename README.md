#  Shipping Confirmation System for Warehouse Accuracy

This project was created as a practical solution to improve **box shipping accuracy** in a warehouse environment, specifically inspired by real problems observed at Target. The system helps verify product quantities, label confirmation, and box fit before items are accepted for shipping.

##  Purpose

In warehouse operations, mislabeled boxes, incorrect quantities, and improperly packed items cause delays and inefficiencies. This tool ensures that:

- Product quantities match expected values.
- Packaging formats are clearly entered and validated.
- Labeling is verified.
- Items fit in the assigned box.

## Features

- GUI built with **Tkinter** for ease of use.
- Input product quantities using total units or `packages/units per package` format.
- Checkbox to verify if the labeling was confirmed.
- Radio buttons to confirm if the items fit in the box.
- Automatic validation against a set of expected product quantities.
- Records each transaction in a **MySQL** database for auditing.

##  Technologies Used

- Python 3  
- Tkinter (GUI)  
- MySQL Connector (Database)


