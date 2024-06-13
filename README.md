
# Campus Distance Calculator CLI

This is a command-line application that calculates distances and durations from a given address to specified campus locations using the Google Maps API.

## Features

- Calculate distances and travel durations from a given address to campuses of North-West University and the University of Johannesburg.
- Supports both driving and walking modes.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/campus_distance_calculator.git
    cd campus_distance_calculator
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scriptsctivate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Google Maps API key:
    - Create a `.env` file in the project root directory.
    - Add your API key to the `.env` file:
      ```env
      GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
      ```

5. Install the package in editable mode:
    ```bash
    pip install -e .
    ```

## Usage

To calculate distances and durations from a given address to each campus:

```bash
calculate_distances "Your street address here"
```

### Example

```bash
calculate_distances "3263 Peace Street Unit 10"
```

### Sample Output

```
North-West University:

  Mafikeng Campus:
    Driving:
      Distance: 4,360 km
      Duration: 48 hours 5 mins
    Walking:
      Distance: 4,255 km
      Duration: 883 hours 21 mins

  Potchefstroom Campus:
    Driving:
      Distance: 4,368 km
      Duration: 48 hours 15 mins
    Walking:
      Distance: 4,262 km
      Duration: 884 hours 45 mins

  Vanderbijlpark Campus:
    Driving:
      Distance: 4,350 km
      Duration: 47 hours 50 mins
    Walking:
      Distance: 4,244 km
      Duration: 881 hours 59 mins

University of Johannesburg:

  Kingsway Campus:
    Driving:
      Distance: 4,364 km
      Duration: 48 hours 10 mins
    Walking:
      Distance: 4,259 km
      Duration: 884 hours 15 mins

  Bunting Road Campus:
    Driving:
      Distance: 4,362 km
      Duration: 48 hours 9 mins
    Walking:
      Distance: 4,257 km
      Duration: 883 hours 55 mins

  Doornfontein Campus:
    Driving:
      Distance: 4,367 km
      Duration: 48 hours 14 mins
    Walking:
      Distance: 4,262 km
      Duration: 884 hours 50 mins

  Soweto Campus:
    Driving:
      Distance: 4,370 km
      Duration: 48 hours 17 mins
    Walking:
      Distance: 4,265 km
      Duration: 885 hours 10 mins
```

## Testing

To run the tests:

```bash
pytest
```

## Project Structure

```
campus_distance_calculator/
│
├── distance_calculator/
│   ├── __init__.py
│   ├── calculator.py
│   ├── cli.py
│   ├── google_maps.py
│   └── settings.py
│
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any changes or improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
