# Setup the board on Mac

## Conda

Create a new environment
```sh
conda create -n coralboard
conda activate coralboard
```

## Python 3.8
> Until [TensorFlow 2](https://www.tensorflow.org/install) supports Python 3.9

```sh
conda install python=3.8
```

## MDT (Mendel Development Tool)
> Official guide [here](https://www.coral.ai/docs/dev-board-mini/get-started/)

The package is not available in the Anaconda repo, so we'll use pip to install in the conda environment [(blog)](https://www.anaconda.com/blog/using-pip-in-a-conda-environment)

```sh
pip install mendel-development-tool
```

