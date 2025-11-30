# 📚 Librarian CLI

A robust command-line tool for managing fixed-width financial transaction files.

##  Setup & Initialization

Ensure dependencies are installed and initialize the database before first use.

```bash
# Initialize the database
python3 librarian/dev/database_init.py                             
```

## Usage

All commands are run via `python3 docsli/src/__main__.py [COMMAND]`.

### 1. File Management
| Command | Description | Example |
| :--- | :--- | :--- |
| **`create-file`** | Create a new file with a header and initial transaction. | `create-file John Doe "Pat" "NY_City" 1000 USD` |
| **`list-files`** | View all files in strict fixed-width format (Colored). | `list-files` |
| **`delete-file`** | Delete a file and all its transactions. | `delete-file 1` |

### 2. Transaction Management
| Command | Description | Example |
| :--- | :--- | :--- |
| **`add-transaction`** | Add a new transaction to an existing file. | `add-transaction 1 500 EUR` |
| **`delete-transaction`** | Remove a specific transaction. | `delete-transaction 1 2` |

### 3. Data Manipulation
| Command | Description | Example |
| :--- | :--- | :--- |
| **`get-value`** | Read a specific field from the database. | `get-value 1 address` |
| **`update-value`** | Update a Header or Footer field. | `update-value 1 surname "Smith"` |
| **`update-value --tx-id`**| Update a specific Transaction field. | `update-value 1 amount 200 --tx-id 5` |

### 4. Configuration
| Command | Description | Example |
| :--- | :--- | :--- |
| **`lock-field`** | Lock a field to prevent future updates. | `lock-field name` |
| **`lock-field --no-locked`**| Unlock a previously locked field. | `lock-field name --no-locked` |

##  Notes
*   **Amounts**: Integers representing cents (e.g., `100` = `1.00`).
*   **Currencies**: Allowed values are `USD`, `EUR`, `PLN`.
*   **Logs**: Operations are logged to `./logger/logs/`.