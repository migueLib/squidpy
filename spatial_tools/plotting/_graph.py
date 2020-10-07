"""Plotting for graph functions
"""

from anndata import AnnData
from typing import Optional, Union
from pandas import DataFrame
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_cluster_centrality_scores(
    adata: AnnData, centrality_scores_key: str = "cluster_centrality_scores"
):
    """
    Plot centrality scores as seaborn stripplot.

    Parameters
    ----------
    adata
        The AnnData object.
    centrality_scores_key
        Key to centrality_scores_key in uns.

    Returns
    -------
    """
    if centrality_scores_key in adata.uns_keys():
        df = adata.uns[centrality_scores_key]
    else:
        raise ValueError(
            "centrality_scores_key %s not recognized. Choose a different key or run first "
            "nhood.cluster_centrality_scores(adata) on your AnnData object."
            % centrality_scores_key
        )

    df = df.rename(
        columns={
            "degree centrality": "degree\ncentrality",
            "clustering coefficient": "clustering\ncoefficient",
            "closeness centrality": "closeness\ncentrality",
            "betweenness centrality": "betweenness\ncentrality",
        }
    )
    values = [
        "degree\ncentrality",
        "clustering\ncoefficient",
        "closeness\ncentrality",
        "betweenness\ncentrality",
    ]
    for i, value in zip([1, 2, 3, 4], values):
        plt.subplot(1, 4, i)
        ax = sns.stripplot(
            data=df, y="cluster", x=value, size=10, orient="h", linewidth=1
        )
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, left=False, right=False, top=False)
        if i > 1:
            plt.ylabel(None)
            ax.tick_params(labelleft=False)


def plot_cluster_interactions(
    adata: AnnData, cluster_interactions_key: str = "cluster_interactions"
):
    """
    Plots cluster interactions as matshow plot.

    Parameters
    ----------
    adata
        The AnnData object.
    cluster_interactions_key
        Key to cluster_interactions_key in uns.

    Returns
    -------
    """
    if cluster_interactions_key in adata.uns_keys():
        interaction_matrix = adata.uns[cluster_interactions_key]
    else:
        raise ValueError(
            "cluster_interactions_key %s not recognized. Choose a different key or run first "
            "nhood.cluster_interactions(adata) on your AnnData object."
            % cluster_interactions_key
        )

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(interaction_matrix[0])
    fig.colorbar(cax)

    plt.xticks(range(len(interaction_matrix[1])), interaction_matrix[1], size="small")
    plt.yticks(range(len(interaction_matrix[1])), interaction_matrix[1], size="small")


def plot_ripley_k(
    adata: AnnData, cluster_key: str, df: Union[DataFrame, None] = None,
):
    """
    Plots Ripley K estimate for each cluster

    Parameters
    ----------
    adata
        The AnnData object.
    cluster_key
        cluster key used to compute ripley's K 
        and stored in adata.uns[f"ripley_k_{cluster_key}"].

    Returns
    -------
    """
    if df is None:
        try:
            df = adata.uns[f"ripley_k_{cluster_key}"]

            try:
                hue_order = [c for c in np.sort(adata.obs[cluster_key].unique())]
                palette = [c for c in adata.uns[f"{cluster_key}_colors"]]
            except ValueError:
                raise Warning(
                    f"\there is no color palette in adata_uns for {cluster_key}\n"
                )

        except ValueError:
            raise ValueError(
                f"\looks like `riply_k_{cluster_key}` was not used\n\n"
                "\is not present in adata.uns,\n"
                "\tplease rerun ripley_k or pass\n"
                "\ta dataframe"
            )
    else:
        hue_order = None
        palette = None

    fig = plt.figure()
    ax = fig.add_subplot(111)
    sns.lineplot(
        "distance",
        "ripley_k",
        hue="leiden",
        hue_order=hue_order,
        data=df,
        palette=palette,
    )
