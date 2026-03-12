# Reflection: Makefile vs run_all.sh

The Makefile makes explicit the dependency relationships between files that run_all.sh left implicit. 
It shows which outputs depend on which inputs, so if a source file changes, only the necessary steps are rerun. 
A new collaborator can immediately see, for example, that updating `code/preprocess.py` triggers figure regeneration and paper recompilation, but not the DID estimation. 
This transparency improves reproducibility and efficiency, and clearly documents the workflow for anyone reading the project.
