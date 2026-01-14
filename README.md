python main.py && python -m experiments.run_gravity_eval

Gravity search

Inputs are treated like “particles”
Bad or interesting behaviors have higher gravity
The search keeps generating inputs near those failures
Over time, the system finds edge cases humans miss
This is closely related to:
Fuzz testing
Evolutionary testing
Property-based testing
Adversarial test generation