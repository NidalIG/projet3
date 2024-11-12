if __name__ == "__main__":
    df = pd.read_csv("medical_examination.csv")
    fig1 = draw_cat_plot(df)
    fig1.savefig("catplot.png")

    fig2 = draw_heat_map(df)
    fig2.savefig("heatmap.png")
