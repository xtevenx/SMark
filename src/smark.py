def display_info(data):
    print("Highest score > {:.2f}".format(max([n * total_score for n in data])))
    print("Lowest score > {:.2f}".format(min([n * total_score for n in data])))
    print("Highest percentage > {:.2f}%".format(max([n * 100 for n in data])))
    print("Lowest percentage > {:.2f}%".format(min([n * 100 for n in data])))
    print()

    print("Average (mean) score > {:.2f}".format(
        stats.mean([n * total_score for n in data])
    ))
    print("Score standard deviation > {:.2f}".format(
        stats.stddev([n * total_score for n in data])
    ))
    print("Average (mean) percentage > {:.2f}%".format(
        stats.mean([n * 100 for n in data])
    ))
    print("Percentage standard deviation > {:.2f}%".format(
        stats.stddev([n * 100 for n in data])
    ))


if __name__ == "__main__":
    import scale
    import stats

    print("SMark Grade Scale Utility", end=2 * "\n")
    total_score = float(input("What is the assignment out of? "))

    print("Enter the individual scores below (one on each line). Enter an empty \n"
          "line after the last input:")
    inputs = []
    while True:
        try:
            inputs.append(float(input()) / total_score)
        except (ValueError, EOFError):
            break

    display_info(inputs)

    print("\n" + "-" * 72 + "\n")
    scale_mean = float(input("What is the target average (mean) percentage? ")) / 100
    scale_f = scale.inverse_power_scale if scale_mean > stats.mean(inputs) else scale.power_scale
    print()

    outputs, sf = scale.scale(inputs, scale_mean, scale_f)
    print("Below are the scaled scores (in the order they were entered):")
    print("\n".join("{:.2f}".format(total_score * n) for n in outputs))
    print()

    display_info(outputs)
