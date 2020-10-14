if __name__ != "__main__":
    print("Error: SMark is a standalone script.")
    exit(0)

import display
import scale
import stats

display.display_header("SMark Grade Scale Utility")

print()
total_score = float(input("What is the assignment out of> "))

print()
print("Enter the individual scores below (one on each line). Enter an empty \n"
      "line after the last input:")

inputs = []
try:
    while True:
        inputs.append(float(input()) / total_score)
except (ValueError, EOFError):
    ...

display.display_info(inputs, total_score, header="input data statistics")

print()
scale_mean = float(input("What is the target average (mean) percentage (0-100)> ")) / 100

scale_func = scale.inverse_power_scale if scale_mean > stats.mean(inputs) else scale.power_scale
outputs, _ = scale.scale(inputs, scale_mean, scale_func)

print()
print("Below are the scaled scores (in the order they were entered):")
print("\n".join("{:.2f}".format(total_score * n) for n in outputs))

print()
display.display_info(outputs, total_score, header="output data statistics")
