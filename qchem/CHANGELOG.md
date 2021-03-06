# Release 0.11.0 (development release)

<h3>New features since last release</h3>

* The function ``get_spinZ_matrix_elements`` has been added to the
  ``obs`` module to generate the matrix elements required to build
  the total-spin projection operator by using the generic function
  ``observable`` as implemented in the same module.
  [(#696)](https://github.com/XanaduAI/pennylane/pull/696)

* The new module ``obs`` has been added to build many-body operators
  whose expectation values can be computed in PennyLane to simulate
  properties of interest of quantum systems. In particular, this PR adds
  the required functions to build the total-spin operator S^2. The adopted
  methodology is very general and is not restricted to molecular systems.
  [(#689)](https://github.com/XanaduAI/pennylane/pull/689)

* The new function ``excitations_to_wires`` has been implemented to map the particle-hole
  representations ph and pphh, generated by ``sd_excitations``, to the wires that the
  qchem templates act on. This implementation enables compliance with the
  generalized PennyLane templates required to build the UCCSD VQE ansatz.
  [(#679)](https://github.com/XanaduAI/pennylane/pull/679)

  For example:

  ```pycon
  >>> n_electrons = 2
  >>> n_spinorbitals = 4
  >>> ph_confs, pphh_confs = sd_excitations(n_electrons, n_spinorbitals)
  >>> print(ph_confs)
  [[0, 2], [1, 3]]
  >>> print(pphh_confs)
  [[0, 1, 2, 3]]

  >>> wires=['a0', 'b1', 'c2', 'd3']
  >>> ph, pphh = excitations_to_wires(ph_confs, pphh_confs, wires=wires)
  >>> print(ph)
  [['a0', 'b1', 'c2'], ['b1', 'c2', 'd3']]
  >>> print(pphh)
  [[['a0', 'b1'], ['c2', 'd3']]]
  ```
<h3>Improvements</h3>

<h3>Breaking changes</h3>

<h3>Documentation</h3>

<h3>Bug fixes</h3>

<h3>Contributors</h3>

This release contains contributions from (in alphabetical order):

Juan Miguel Arrazola, Alain Delgado, Josh Izaac, Soran Jahangiri, Maria Schuld

# Release 0.10.0 (current release)

<h3>New features since last release</h3>

* The function ``hf_state`` outputs an array with the occupation-number
  representation of the Hartree-Fock (HF) state. This function can be used to
  set the qubit register to encode the HF state which is the typical starting
  point for quantum chemistry simulations using the VQE algorithm.
  [(#629)](https://github.com/XanaduAI/pennylane/pull/629)

<h3>Improvements</h3>

* The function ``convert_hamiltonian`` has been renamed to ``convert_observable``
  since it can be used to convert any OpenFermion QubitOperator to a PennyLane
  Observable. ``convert_observable`` will be used in the ``obs`` module to build
  observables linked to molecular properties.
  [(#677)](https://github.com/XanaduAI/pennylane/pull/677)

<h3>Breaking changes</h3>

* Removes support for Python 3.5.
  [(#639)](https://github.com/XanaduAI/pennylane/pull/639)

<h3>Contributors</h3>

This release contains contributions from (in alphabetical order):

Juan Miguel Arrazola, Alain Delgado, Josh Izaac, Soran Jahangiri, Maria Schuld

# Release 0.9.0

Initial release.
