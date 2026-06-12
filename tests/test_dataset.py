import numpy as np
import pytest

import pyLasaDataset as lasa


def test_names_available():
    names = lasa.DataSet.names
    assert len(names) == 30
    assert "Angle" in names
    assert "Sine" in names


def test_load_pattern():
    angle = lasa.DataSet.Angle
    assert angle.name == "Angle"
    assert angle.dt > 0
    assert len(angle.demos) == 7
    for demo in angle.demos:
        assert isinstance(demo.pos, np.ndarray)
        assert demo.pos.shape[0] == 2
        assert demo.pos.shape == demo.vel.shape == demo.acc.shape
        assert demo.t.shape == (1, demo.pos.shape[1])


def test_unknown_pattern_raises():
    with pytest.raises(AttributeError, match="NotARealPattern"):
        lasa.DataSet.NotARealPattern


def test_loaded_data_is_cached():
    assert lasa.DataSet.Angle is lasa.DataSet.Angle


def test_plot_model_smoke(monkeypatch):
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", lambda: None)
    lasa.utilities.plot_model(lasa.DataSet.Angle)
    plt.close("all")
