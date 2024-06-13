import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# TODO: write as a function

score_used = "mse"
models_comparison_folder_path = "models/models_comparison"
scores_dictionnary_filename = "autoencoders_score"
save_fig_filename = f"models_comparison_{score_used}"
if __name__ == "__main__":

    with open(
        f"{models_comparison_folder_path}/{scores_dictionnary_filename}.pkl", "rb"
    ) as f:
        models_eval = pickle.load(f)

    results_df = pd.DataFrame(list(models_eval.items()), columns=["Model", "Score"])
    results_df = results_df.sort_values(by="Score", ascending=True)

    plt.figure(figsize=(10, 6))
    sns.barplot(results_df, y="Score", x="Model", color="steelblue")
    plt.ylabel(score_used)
    plt.tight_layout()
    plt.savefig(f"{models_comparison_folder_path}/{save_fig_filename}.png")
    plt.show()
