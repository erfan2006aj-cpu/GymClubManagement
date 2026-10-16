# Gym Club Management System

A Python-based command-line application for managing gym operations. The system provides separate workflows for managers, coaches, and members, covering user management, gym halls, classes, registrations, subscriptions, wallet transactions, and workout plans.

The project follows a modular structure that separates user interfaces, business logic, data models, and file operations. Application data is stored in a shared text file.

## Features

### User Management and Authentication

- Role-based login flows for managers, coaches, and members.
- User creation and account management.
- Account activation and deactivation.
- Input validation for usernames, passwords, and email addresses.

### Gym Management

- Create and manage gym halls.
- Create and manage gym classes.
- Assign coaches and halls to classes.
- Manage class availability.

### Class Registration

- Register members for classes.
- Cancel class registrations.
- Retrieve registration information for members and classes.
- Generate tracking numbers for registrations.

### Subscription Management

- Monthly, three-month, and six-month subscription plans.
- Subscription start and end dates.
- Retrieve active subscriptions and subscription status.
- View subscriptions by member.
- Calculate total subscription income.

### Wallet and Transactions

- Retrieve member wallet balances.
- Add funds to a wallet through a simulated payment API.
- Pay for subscriptions using wallet funds.
- Store financial transaction records.
- Retrieve transaction history for individual members.

### Workout Management

- Create and manage workout plans.
- Add, edit, and remove exercises.
- Retrieve workout plans by coach or member.

## Technologies

- **Python** — application logic and command-line interface.
- **Object-oriented programming** — models and service classes.
- **Text-file storage** — persistent application data.
- **Regular expressions** — input validation.
- **Python standard library** — file paths, date handling, and other utility operations.

The project does not require a separate database server.

## Getting Started

### Prerequisites

- Python installed on your system.
- Git, if you want to clone the repository.

### Installation

Clone the repository:

```bash
git clone https://github.com/erfan2006aj-cpu/GymClubManagement.git
cd GymClubManagement
```

### Running the Application

Run the following command from the project root:

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

The application displays a command-line menu through which users can access the available manager, coach, and member workflows.

## Project Structure

```text
GymClubManagement/
├── bank/
│   ├── __init__.py
│   └── Bank.py
├── data/
│   └── gym_data.txt
├── docs/
│   └── flowcharts/
│       └── README.md
├── gym/
│   ├── __init__.py
│   ├── constants.py
│   ├── decorators.py
│   ├── exceptions.py
│   ├── models.py
│   ├── storage.py
│   ├── utils.py
│   ├── validators.py
│   ├── menus/
│   │   ├── manager_menu.py
│   │   ├── member_menu.py
│   │   ├── start_menu.py
│   │   └── trainer_menu.py
│   └── services/
│       ├── auth.py
│       ├── classes.py
│       ├── halls.py
│       ├── registrations.py
│       ├── subscriptions.py
│       ├── users.py
│       ├── wallet.py
│       └── workout.py
└── main.py
```

## Architecture

The application is organized into modules with distinct responsibilities.

- **`main.py`** — starts the application and routes users to the appropriate login flow and menu.
- **`gym/menus/`** — contains the command-line interfaces for managers, coaches, and members.
- **`gym/services/`** — implements authentication, user management, halls, classes, registrations, subscriptions, wallet operations, and workout plans.
- **`gym/models.py`** — defines the application's domain models.
- **`gym/storage.py`** — provides reusable text-file operations through the `Storage` class.
- **`gym/validators.py`** — contains input-validation functions.
- **`gym/exceptions.py`** — defines application-specific exceptions.
- **`gym/utils.py`** — contains shared utility functions.
- **`bank/Bank.py`** — provides a simulated local payment API.

## Data Storage

Application data is stored in:

```text
data/gym_data.txt
```

The shared text file contains categorized records for entities such as users, halls, classes, registrations, subscriptions, and transactions.

Section markers separate different record categories. Individual services interpret and update their corresponding records, while the `Storage` class provides the underlying file operations.

The project uses file-based persistence rather than a relational database. It does not provide database-level transactions, concurrency control, or database integrity constraints.

## Subscription Plans

The subscription service defines the following plans:

| Plan | Duration |
|---|---:|
| Monthly | 30 days |
| Three Months | 90 days |
| Six Months | 180 days |

Subscription prices and durations are defined in the application code.

## Limitations

The current implementation is intended as a command-line software project and is not designed for production use with real customer or financial data.

- **File-based persistence:** Application data is stored in a shared text file rather than a database.
- **Simulated payments:** Payment processing does not use a real banking service.
- **Security:** Additional security measures are needed before the application can safely handle real user accounts and financial information.
- **Automated testing:** No automated test suite is included in the current project structure.
- **Activity logging:** The `gym/decorators.py` file exists, but a logging decorator has not been implemented in the current version.

## Future Improvements

- Migrate from text-file storage to a database such as SQLite.
- Improve password security and authentication.
- Integrate a secure, real payment provider.
- Add automated unit and integration tests.
- Implement structured logging and activity auditing.
- Improve configuration management and data consistency.

## Project Status

Gym Club Management System is a modular command-line application for managing core gym operations. Its current implementation focuses on role-based workflows, service-level business logic, and text-file persistence.