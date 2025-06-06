from simulation import *
from visual import *
import re

def get_positive_float_input(prompt, allow_zero=False):
    while True:
        try:
            value = float(input(prompt))
            if (value > 0) or (allow_zero and value == 0):
                return value
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def parse_equation(equation):
    term_pattern = r'([+-]?\d*\.?\d*)\s*([A-Z])?([A-Z])?'
    terms = re.findall(term_pattern, equation.replace(" ", ""))

    #print(terms)

    growth_rate = 0
    control_rate = 0
    prey_letter = None
    predator_letter = None

    for coefficient, var1, var2 in terms:
        # No stated numerical coefficient (-F or +R)
        if coefficient in ["", "+"]:
            coefficient = 1.0
        elif coefficient == "-":
            coefficient = -1.0
        else:
            coefficient = float(coefficient)

        if var1 and not var2:
            if prey_letter is None:
                growth_rate = coefficient
                prey_letter = var1
            else:
                predator_letter = var1

        elif var1 and var2:
            control_rate = coefficient
            prey_letter = var1
            predator_letter = var2

    if not predator_letter and prey_letter:
        predator_letter = prey_letter
        prey_letter = None

    if not prey_letter or not predator_letter:
        raise ValueError("Invalid equation format. Ensure it contains prey and predator terms.")

    #print(growth_rate, control_rate, prey_letter, predator_letter)

    return growth_rate, control_rate, prey_letter, predator_letter

def set_up_prey_predator():
    while True:
        try:
            prey_equation = input("Enter the prey equation: ")
            prey_growth_rate, prey_control_rate, prey_letter, predator_letter = parse_equation(prey_equation)

            predator_equation = input("Enter the predator equation: ")
            predator_growth_rate, predator_control_rate, predator_prey_letter, predator_predator_letter = parse_equation(
                predator_equation)

            if prey_letter != predator_prey_letter or predator_letter != predator_predator_letter:
                print(f"Error: The variables in the equations must match. "
                      f"Expected '{prey_letter}' and '{predator_letter}', but got '{predator_prey_letter}' and '{predator_predator_letter}'.")
                continue

            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    prey = Prey(prey_growth_rate, prey_control_rate, prey_letter, predator_letter)

    predator = Predator(predator_growth_rate, predator_control_rate, prey_letter, predator_letter)

    return prey, predator

def set_up_euler(prey, predator):
    print("\nEnter parameters for the Equation:")

    initial_prey_population = get_positive_float_input("Initial prey population: ")
    initial_predator_population = get_positive_float_input("Initial predator population: ")
    time_step = get_positive_float_input("Time step (e.g., 0.5): ")
    #start_time = get_positive_float_input("Start time (e.g., 0): ", allow_zero=True)
    #final_time = get_positive_float_input("Final time (must be greater than start time): ")
    final_time = get_positive_float_input("Final time (must be greater than 0): ")

    #while final_time <= start_time:
    while final_time <= 0:
        print("Final time must be greater than start time.")
        final_time = get_positive_float_input("Final time (must be greater than start time): ")

    #euler = Euler(initial_prey_population, initial_predator_population, prey, predator, time_step, start_time, final_time)
    euler = Euler(initial_prey_population, initial_predator_population, prey, predator, time_step, 0,
                  final_time)

    return euler

def set_up_runge_kutta(prey, predator):
    print("\nEnter parameters for the Equation:")

    initial_prey_population = get_positive_float_input("Initial prey population: ")
    initial_predator_population = get_positive_float_input("Initial predator population: ")
    time_step = get_positive_float_input("Time step (e.g., 0.5): ")
    #start_time = get_positive_float_input("Start time (e.g., 0): ", allow_zero=True)
    #final_time = get_positive_float_input("Final time (must be greater than start time): ")
    final_time = get_positive_float_input("Final time (must be greater than 0): ")

    # while final_time <= start_time:
    while final_time <= 0:
        print("Final time must be greater than start time.")
        final_time = get_positive_float_input("Final time (must be greater than start time): ")

    #rk = RungeKutta(initial_prey_population, initial_predator_population, prey, predator, time_step, start_time, final_time)
    rk = RungeKutta(initial_prey_population, initial_predator_population, prey, predator, time_step, 0,
                    final_time)

    return rk

def main():
    prey, predator = set_up_prey_predator()

    method_choice = input("\nChoose simulation method: (E)uler or (R)unge-Kutta? ").strip().upper()
    while method_choice not in ['E', 'R']:
        print("Invalid choice. Please enter E for Euler or R for Runge-Kutta.")
        method_choice = input("Choose simulation method: (E)uler or (R)unge-Kutta? ").strip().upper()

    if method_choice == 'E':
        simulation = set_up_euler(prey, predator)
    else:
        simulation = set_up_runge_kutta(prey, predator)

    print(f"\nSimulation Object: {simulation}")

    display_choice = input("\nDisplay results as (T)able or (G)raph? ").strip().upper()
    while display_choice not in ['T', 'G']:
        print("Invalid choice. Please enter T for Table or G for Graph.")
        display_choice = input("Display results as (T)able or (G)raph? ").strip().upper()

    if display_choice == 'T':
        table_data = simulation.calculate_table()
        simulation.print_table(table_data)
    else:
        points_data = simulation.calculate_points()
        draw_graph(points_data)

def main_test():
    prey = Prey(3, -1.4, "R", "F")

    predator = Predator(-1, .8, "R", "F")

    euler = Euler(1, 1, prey, predator, .05, 0,
                 12)

    print(euler)

if __name__ == '__main__':
    main_test()
