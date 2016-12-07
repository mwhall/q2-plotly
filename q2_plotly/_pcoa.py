import os
import os.path
import pkg_resources

import skbio
import pandas as pd
import plotly
from plotly.graph_objs import Scatter, Layout
import qiime
import q2templates
from q2_types import PCoAResults

#Fiz the location of the directory containing the template HTML files
TEMPLATES = pkg_resources.resource_filename("q2_plotly", 'assets')

def pcoa(output_dir: str, metadata: qiime.Metadata,
                pcoa: skbio.OrdinationResults) -> None:
   
    #For some reason, we take in the pcoa object as a skbio.OrdinationResults here
    #despite it being defined as a q2_types PCoAResults in the input...
    #I'll have to ask the devs why, I just copied it from an example.

    #Start off basic while I'm learning this, look only at PC1 and PC2
    pc1 = pcoa.samples.values[:,0]
    pc2 = pcoa.samples.values[:,1]

    prop_exp1 = pcoa.proportion_explained[0]
    prop_exp2 = pcoa.proportion_explained[1]

    #Transform qiime.Metadata class into pandas dataframe
    metadata_df = metadata.to_dataframe()

    #Generate the menu dict for the Plotly dropdown
    #Note: The way this works, we don't get a legend,
    # because everything is in one trace
    # An alternative would be to make each metadata category
    # a trace, but this would be a huge amount of traces
    # and doesn't seem like a good idea, but may be the only
    # option with Plotly coded as it is now.
    metadata_menus = []
    for md in metadata_df.columns:
        md_vals = metadata_df[md]
        md_vals = md_vals.loc[pcoa.samples.index]
        #Map the metadata values to integers
        r = range(0,len(set(md_vals)))
        intmap = dict(zip(set(md_vals),r))
        cols = [intmap[y] for y in md_vals]
        eprint(cols)
        menu_dict = dict(args=['marker', dict(color=cols)],
                         label=md,
                         method='restyle')
        metadata_menus.append(menu_dict)
     
    #Grab the location of our base index.html file   
    index = os.path.join(TEMPLATES, 'index.html')
    
    #Generate the plot with Plotly offline, export as HTML (div)
    main_plot = plotly.offline.plot({
                    "data": [Scatter(x=pc1, y=pc2, mode='markers')],
                    "layout": Layout(title="PCoA Ordination",
                                     xaxis=dict(title="PC1 (%.2f%)"%prop_exp1),
                                     yaxis=dict(title="PC2 (%.2f%)"%prop_exp2),
                                     updatemenus=list([
                                         dict(
                                             x=-0.1,
                                             y=1,
                                             buttons=metadata_menus,
                                             yanchor='top'
                                         )
                                     ])
                                    )
                    },
                    output_type="div", auto_open=False, image="svg")

    #These are the items that end up in the visualizer
    context = {
        "main_plot": main_plot
    }
    #Extend the index.html file in assets
    q2templates.render(index, output_dir, context=context)

