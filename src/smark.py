import sys

if __name__ != "__main__":
    print("Error: SMark is a standalone script.")
    sys.exit(1)

import display
import scale
import stats

display.display_header("SMark Grade Scale Utility")

print()
total_score = display.input_float(
    prompt="What is the assignment out of> ",
    qualifier=lambda x: x > 0,
    qualifier_err="Error: please input a positive number."
)

print()
print("Enter the individual scores below (one on each line). Enter an empty \n"
      "line after the last input:")

inputs = []
try:
    while this_input := input().strip():
        decimal_input = float(this_input) / total_score
        if not 0 <= decimal_input <= 1:
            raise AssertionError
        inputs.append(decimal_input)

except ValueError:
    ordinals = ["st", "nd", "rd"] + ["th"] * 7
    formatted_num = f"{len(inputs) + 1}{ordinals[len(inputs) % 10]}"
    print(f"Error: could not parse the {formatted_num} input.")
    sys.exit(1)

except AssertionError:
    ordinals = ["st", "nd", "rd"] + ["th"] * 7
    formatted_num = f"{len(inputs) + 1}{ordinals[len(inputs) % 10]}"
    total_score = int(total_score) if round(total_score) == total_score else total_score
    print(f"Error: the {formatted_num} input is not in range (0 - {total_score}).")
    sys.exit(1)

display.display_info(inputs, total_score, header="input data statistics")

print()
scale_mean = display.input_float(
    prompt="What is the target average (mean) percentage (0 - 100)> ",
    qualifier=lambda x: 0 <= x <= 100,
    qualifier_err="Error: please input a number between 0 and 100."
) / 100

scale_func = scale.inverse_power_scale if scale_mean > stats.mean(inputs) else scale.power_scale
outputs, _ = scale.scale(inputs, scale_mean, scale_func)

print()
print("Below are the scaled scores (in the order they were entered):")
print("\n".join("{:.2f}".format(total_score * n) for n in outputs))

print()
display.display_info(outputs, total_score, header="output data statistics")
