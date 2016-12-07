#Import our own library
import q2_plotly
#Grab the function we want to register from the local file
from ._pcoa import pcoa

import qiime.plugin
#We need this class as input
from q2_types import PCoAResults

# Basic plugin-wide information
plugin = qiime.plugin.Plugin(
    name='plotly',
    version=q2_plotly.__version__,
    website='None',
    package='q2_plotly',
    # Information on how to obtain user support should be provided as a free
    # text string via user_support_text. If None is provided, users will
    # be referred to the plugin's website for support.
    user_support_text=None,
    # Information on how the plugin should be cited should be provided as a
    # free text string via citation_text. If None is provided, users
    # will be told to use the plugin's website as a citation.
    citation_text=None
)

# This registers the function with QIIME2 
plugin.visualizers.register_function(
    function=pcoa,
    # Note: We require the q2_types.PCoAResults type here
    # but in the _pcoa.pcoa function signature, it needs to be
    # skbio.OrdinationResults??
    inputs={
        'pcoa': PCoAResults
    },
    # Similarly, this needs to be qiime.plugin.Metadata here
    # but has to be qiime.Metadata in the function signature
    # and I have no clue why
    parameters={
        'metadata': qiime.plugin.Metadata
    },
    name='Visualize PCoA results',
    description='This visualizer produces an offline Plotly plot of'
                'a PCoA ordination'
)
