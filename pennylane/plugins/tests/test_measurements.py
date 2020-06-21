# Copyright 2018-2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests that the different measurement types work correctly on a device."""
import numpy as np
import pennylane as qml
from flaky import flaky

# ==========================================================
# Some useful global variables

# single qubit Hermitian observable
A = np.array([[1.02789352, 1.61296440 - 0.3498192j], [1.61296440 + 0.3498192j, 1.23920938 + 0j]])


@flaky(max_runs=10)
class TestExpval:
    """Test expectation values"""

    def test_identity_expectation(self, device, tol, skip_if):
        """Test that identity expectation value (i.e. the trace) is 1."""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.Identity(wires=0)), qml.expval(qml.Identity(wires=1))

        res = circuit()
        assert np.allclose(res, np.array([1, 1]), atol=tol(dev.analytic))

    def test_pauliz_expectation(self, device, tol, skip_if):
        """Test that PauliZ expectation value is correct"""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.PauliZ(wires=0)), qml.expval(qml.PauliZ(wires=1))

        res = circuit()
        assert np.allclose(
            res, np.array([np.cos(theta), np.cos(theta) * np.cos(phi)]), atol=tol(dev.analytic)
        )

    def test_paulix_expectation(self, device, tol, skip_if):
        """Test that PauliX expectation value is correct"""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123

        @qml.qnode(dev)
        def circuit():
            qml.RY(theta, wires=[0])
            qml.RY(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.PauliX(wires=0)), qml.expval(qml.PauliX(wires=1))

        res = circuit()
        expected = np.array([np.sin(theta) * np.sin(phi), np.sin(phi)])
        print(type(res), res)
        print(type(expected), expected)
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_pauliy_expectation(self, device, tol, skip_if):
        """Test that PauliY expectation value is correct"""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.PauliY(wires=0)), qml.expval(qml.PauliY(wires=1))

        res = circuit()
        expected = np.array([0.0, -np.cos(theta) * np.sin(phi)])
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_hadamard_expectation(self, device, tol, skip_if):
        """Test that Hadamard expectation value is correct"""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123

        @qml.qnode(dev)
        def circuit():
            qml.RY(theta, wires=[0])
            qml.RY(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.Hadamard(wires=0)), qml.expval(qml.Hadamard(wires=1))

        res = circuit()
        expected = np.array(
            [np.sin(theta) * np.sin(phi) + np.cos(theta), np.cos(theta) * np.cos(phi) + np.sin(phi)]
        ) / np.sqrt(2)
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_hermitian_expectation(self, device, tol, skip_if):
        """Test that arbitrary Hermitian expectation values are correct"""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123

        @qml.qnode(dev)
        def circuit():
            qml.RY(theta, wires=[0])
            qml.RY(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.Hermitian(A, wires=0)), qml.expval(qml.Hermitian(A, wires=1))

        res = circuit()

        a = A[0, 0]
        re_b = A[0, 1].real
        d = A[1, 1]
        ev1 = ((a - d) * np.cos(theta) + 2 * re_b * np.sin(theta) * np.sin(phi) + a + d) / 2
        ev2 = ((a - d) * np.cos(theta) * np.cos(phi) + 2 * re_b * np.sin(phi) + a + d) / 2
        expected = np.array([ev1, ev2])

        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_multi_mode_hermitian_expectation(self, device, tol, skip_if):
        """Test that arbitrary multi-mode Hermitian expectation values are correct"""
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        A = np.array(
            [
                [-6, 2 + 1j, -3, -5 + 2j],
                [2 - 1j, 0, 2 - 1j, -5 + 4j],
                [-3, 2 + 1j, 0, -4 + 3j],
                [-5 - 2j, -5 - 4j, -4 - 3j, -6],
            ]
        )

        @qml.qnode(dev)
        def circuit():
            qml.RY(theta, wires=[0])
            qml.RY(phi, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.Hermitian(A, wires=[0, 1]))

        res = circuit()

        # below is the analytic expectation value for this circuit with arbitrary
        # Hermitian observable A
        expected = 0.5 * (
            6 * np.cos(theta) * np.sin(phi)
            - np.sin(theta) * (8 * np.sin(phi) + 7 * np.cos(phi) + 3)
            - 2 * np.sin(phi)
            - 6 * np.cos(phi)
            - 6
        )

        assert np.allclose(res, expected, atol=tol(dev.analytic))


@flaky(max_runs=10)
class TestTensorExpval:
    """Test tensor expectation values"""

    def test_paulix_pauliy(self, device, tol, skip_if):
        """Test that a tensor product involving PauliX and PauliY works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(phi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.expval(qml.PauliX(wires=0)), qml.expval(qml.PauliX(wires=2))

        res = circuit()

        expected = np.sin(theta) * np.sin(phi) * np.sin(varphi)
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_pauliz_hadamard(self, device, tol, skip_if):
        """Test that a tensor product involving PauliZ and PauliY and hadamard works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(phi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return (
                qml.expval(qml.PauliZ(wires=0)),
                qml.expval(qml.Hadamard(wires=1)),
                qml.expval(qml.PauliY(wires=2)),
            )

        res = circuit()

        expected = -(np.cos(varphi) * np.sin(phi) + np.sin(varphi) * np.cos(theta)) / np.sqrt(2)
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_hermitian(self, device, tol, skip_if):
        """Test that a tensor product involving qml.Hermitian works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543
        A = np.array(
            [
                [-6, 2 + 1j, -3, -5 + 2j],
                [2 - 1j, 0, 2 - 1j, -5 + 4j],
                [-3, 2 + 1j, 0, -4 + 3j],
                [-5 - 2j, -5 - 4j, -4 - 3j, -6],
            ]
        )

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(phi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.expval(qml.PauliZ(wires=0)), qml.expval(qml.Hermitian(A, wires=[1, 2]))

        res = circuit()

        expected = 0.5 * (
            -6 * np.cos(theta) * (np.cos(varphi) + 1)
            - 2 * np.sin(varphi) * (np.cos(theta) + np.sin(phi) - 2 * np.cos(phi))
            + 3 * np.cos(varphi) * np.sin(phi)
            + np.sin(phi)
        )
        assert np.allclose(res, expected, atol=tol(dev.analytic))


@flaky(max_runs=10)
class TestSample:
    """Tests for the sample return type."""

    def test_sample_values(self, device, tol, skip_if):
        """Tests if the samples returned by sample have
        the correct values
        """
        n_wires = 1
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        @qml.qnode(dev)
        def circuit():
            qml.RX(1.5708, wires=[0])
            return qml.sample(qml.PauliZ(wires=0))

        res = circuit()

        # res should only contain 1 and -1
        assert np.allclose(res ** 2, 1, atol=tol(False))

    def test_sample_values_hermitian(self, device, tol, skip_if):
        """Tests if the samples of a Hermitian observable returned by sample have
        the correct values
        """
        n_wires = 1
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        A = np.array([[1, 2j], [-2j, 0]])
        theta = 0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            return qml.sample(qml.Hermitian(A, wires=0))

        res = circuit()

        # res should only contain the eigenvalues of
        # the hermitian matrix
        eigvals = np.linalg.eigvalsh(A)
        assert np.allclose(sorted(list(set(res))), sorted(eigvals), atol=tol(dev.analytic))
        # the analytic mean is 2*sin(theta)+0.5*cos(theta)+0.5
        assert np.allclose(
            np.mean(res), 2 * np.sin(theta) + 0.5 * np.cos(theta) + 0.5, atol=tol(False)
        )
        # the analytic variance is 0.25*(sin(theta)-4*cos(theta))^2
        assert np.allclose(
            np.var(res), 0.25 * (np.sin(theta) - 4 * np.cos(theta)) ** 2, atol=tol(False)
        )

    def test_sample_values_hermitian_multi_qubit(self, device, tol, skip_if):
        """Tests if the samples of a multi-qubit Hermitian observable returned by sample have
        the correct values
        """
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.543
        A = np.array(
            [
                [1, 2j, 1 - 2j, 0.5j],
                [-2j, 0, 3 + 4j, 1],
                [1 + 2j, 3 - 4j, 0.75, 1.5 - 2j],
                [-0.5j, 1, 1.5 + 2j, -1],
            ]
        )

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RY(2 * theta, wires=[1])
            qml.CNOT(wires=[0, 1])
            return qml.sample(qml.Hermitian(A, wires=[0, 1]))

        res = circuit()

        # res should only contain the eigenvalues of
        # the hermitian matrix
        eigvals = np.linalg.eigvalsh(A)
        assert np.allclose(sorted(list(set(res))), sorted(eigvals), atol=tol(dev.analytic))

        # make sure the mean matches the analytic mean
        expected = (
            88 * np.sin(theta)
            + 24 * np.sin(2 * theta)
            - 40 * np.sin(3 * theta)
            + 5 * np.cos(theta)
            - 6 * np.cos(2 * theta)
            + 27 * np.cos(3 * theta)
            + 6
        ) / 32
        assert np.allclose(np.mean(res), expected, atol=tol(False))


@flaky(max_runs=10)
class TestTensorSample:
    """Test tensor sample values."""

    def test_paulix_pauliy(self, device, tol, skip_if):
        """Test that a tensor product involving PauliX and PauliY works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(varphi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.sample(qml.PauliX(wires=[0]) @ qml.PauliY(wires=[2]))

        res = circuit()

        # res should only contain 1 and -1
        assert np.allclose(res ** 2, 1, atol=tol(dev.analytic))

        mean = np.mean(res)
        expected = np.sin(theta) * np.sin(phi) * np.sin(varphi)
        assert np.allclose(mean, expected, atol=tol(dev.analytic))

        var = np.var(res)
        expected = (
            8 * np.sin(theta) ** 2 * np.cos(2 * varphi) * np.sin(phi) ** 2
            - np.cos(2 * (theta - phi))
            - np.cos(2 * (theta + phi))
            + 2 * np.cos(2 * theta)
            + 2 * np.cos(2 * phi)
            + 14
        ) / 16
        assert np.allclose(var, expected, atol=tol(False))

    def test_pauliz_hadamard(self, device, tol, skip_if):
        """Test that a tensor product involving PauliZ and PauliY and hadamard works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(varphi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.sample(
                qml.PauliZ(wires=[0]) @ qml.Hadamard(wires=[1]) @ qml.PauliY(wires=[2])
            )

        res = circuit()

        # s1 should only contain 1 and -1
        assert np.allclose(res ** 2, 1, atol=tol(dev.analytic))

        mean = np.mean(res)
        expected = -(np.cos(varphi) * np.sin(phi) + np.sin(varphi) * np.cos(theta)) / np.sqrt(2)
        assert np.allclose(mean, expected, atol=tol(dev.analytic))

        var = np.var(res)
        expected = (
            3
            + np.cos(2 * phi) * np.cos(varphi) ** 2
            - np.cos(2 * theta) * np.sin(varphi) ** 2
            - 2 * np.cos(theta) * np.sin(phi) * np.sin(2 * varphi)
        ) / 4
        assert np.allclose(var, expected, atol=tol(False))

    def test_hermitian(self, device, tol, skip_if):
        """Test that a tensor product involving qml.Hermitian works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        A = np.array(
            [
                [-6, 2 + 1j, -3, -5 + 2j],
                [2 - 1j, 0, 2 - 1j, -5 + 4j],
                [-3, 2 + 1j, 0, -4 + 3j],
                [-5 - 2j, -5 - 4j, -4 - 3j, -6],
            ]
        )

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(varphi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.sample(qml.PauliZ(wires=[0]) @ qml.Hermitian(A, wires=[1, 2]))

        res = circuit()

        # res should only contain the eigenvalues of
        # the hermitian matrix tensor product Z
        Z = np.diag([1, -1])
        eigvals = np.linalg.eigvalsh(np.kron(Z, A))
        assert np.allclose(sorted(list(set(res))), sorted(eigvals), atol=tol(dev.analytic))

        mean = np.mean(res)
        expected = 0.5 * (
            -6 * np.cos(theta) * (np.cos(varphi) + 1)
            - 2 * np.sin(varphi) * (np.cos(theta) + np.sin(phi) - 2 * np.cos(phi))
            + 3 * np.cos(varphi) * np.sin(phi)
            + np.sin(phi)
        )
        assert np.allclose(mean, expected, atol=tol(False))

        var = np.var(res)
        expected = (
            1057
            - np.cos(2 * phi)
            + 12 * (27 + np.cos(2 * phi)) * np.cos(varphi)
            - 2 * np.cos(2 * varphi) * np.sin(phi) * (16 * np.cos(phi) + 21 * np.sin(phi))
            + 16 * np.sin(2 * phi)
            - 8 * (-17 + np.cos(2 * phi) + 2 * np.sin(2 * phi)) * np.sin(varphi)
            - 8 * np.cos(2 * theta) * (3 + 3 * np.cos(varphi) + np.sin(varphi)) ** 2
            - 24 * np.cos(phi) * (np.cos(phi) + 2 * np.sin(phi)) * np.sin(2 * varphi)
            - 8
            * np.cos(theta)
            * (
                4
                * np.cos(phi)
                * (
                    4
                    + 8 * np.cos(varphi)
                    + np.cos(2 * varphi)
                    - (1 + 6 * np.cos(varphi)) * np.sin(varphi)
                )
                + np.sin(phi)
                * (
                    15
                    + 8 * np.cos(varphi)
                    - 11 * np.cos(2 * varphi)
                    + 42 * np.sin(varphi)
                    + 3 * np.sin(2 * varphi)
                )
            )
        ) / 16
        assert np.allclose(var, expected, atol=tol(False))


@flaky(max_runs=10)
class TestVar:
    """Tests for the variance return type"""

    def test_var(self, device, tol, skip_if):
        """Tests if the samples returned by sample have
        the correct values
        """
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        phi = 0.543
        theta = 0.6543

        @qml.qnode(dev)
        def circuit():
            qml.RX(phi, wires=[0])
            qml.RY(theta, wires=[0])
            return qml.var(qml.PauliZ(wires=0))

        res = circuit()

        expected = 0.25 * (3 - np.cos(2 * theta) - 2 * np.cos(theta) ** 2 * np.cos(2 * phi))
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_var_hermitian(self, device, tol, skip_if):
        """Tests if the samples of a Hermitian observable returned by sample have
        the correct values
        """
        n_wires = 2
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if(not capabilities["model"] == "qubit")

        phi = 0.543
        theta = 0.6543
        # test correct variance for <H> of a rotated state
        H = 0.1 * np.array([[4, -1 + 6j], [-1 - 6j, 2]])

        @qml.qnode(dev)
        def circuit():
            qml.RX(phi, wires=[0])
            qml.RY(theta, wires=[0])
            return qml.var(qml.Hermitian(H, wires=0))

        res = circuit()

        expected = (
            0.01
            * 0.5
            * (
                2 * np.sin(2 * theta) * np.cos(phi) ** 2
                + 24 * np.sin(phi) * np.cos(phi) * (np.sin(theta) - np.cos(theta))
                + 35 * np.cos(2 * phi)
                + 39
            )
        )

        assert np.allclose(res, expected, atol=tol(dev.analytic))


@flaky(max_runs=10)
class TestTensorVar:
    """Test tensor variance measurements."""

    def test_paulix_pauliy(self, device, tol, skip_if):
        """Test that a tensor product involving PauliX and PauliY works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(varphi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.var(qml.PauliX(wires=[0]) @ qml.PauliY(wires=[2]))

        res = circuit()

        expected = (
            8 * np.sin(theta) ** 2 * np.cos(2 * varphi) * np.sin(phi) ** 2
            - np.cos(2 * (theta - phi))
            - np.cos(2 * (theta + phi))
            + 2 * np.cos(2 * theta)
            + 2 * np.cos(2 * phi)
            + 14
        ) / 16
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_pauliz_hadamard(self, device, tol, skip_if):
        """Test that a tensor product involving PauliZ and PauliY and hadamard works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(varphi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.sample(
                qml.PauliZ(wires=[0]) @ qml.Hadamard(wires=[1]) @ qml.PauliY(wires=[2])
            )

        res = circuit()

        expected = (
            3
            + np.cos(2 * phi) * np.cos(varphi) ** 2
            - np.cos(2 * theta) * np.sin(varphi) ** 2
            - 2 * np.cos(theta) * np.sin(phi) * np.sin(2 * varphi)
        ) / 4
        assert np.allclose(res, expected, atol=tol(dev.analytic))

    def test_hermitian(self, device, tol, skip_if):
        """Test that a tensor product involving qml.Hermitian works correctly"""
        n_wires = 3
        dev = device(n_wires)
        capabilities = dev.__class__.capabilities()
        skip_if("tensor_observable" not in capabilities)
        skip_if("tensor_observable" in capabilities and not capabilities["tensor_observable"])
        skip_if(not capabilities["model"] == "qubit")

        theta = 0.432
        phi = 0.123
        varphi = -0.543

        A = np.array(
            [
                [-6, 2 + 1j, -3, -5 + 2j],
                [2 - 1j, 0, 2 - 1j, -5 + 4j],
                [-3, 2 + 1j, 0, -4 + 3j],
                [-5 - 2j, -5 - 4j, -4 - 3j, -6],
            ]
        )

        @qml.qnode(dev)
        def circuit():
            qml.RX(theta, wires=[0])
            qml.RX(phi, wires=[1])
            qml.RX(varphi, wires=[2])
            qml.CNOT(wires=[0, 1])
            qml.CNOT(wires=[1, 2])
            return qml.sample(qml.PauliZ(wires=[0]) @ qml.Hermitian(A, wires=[1, 2]))

        res = circuit()

        expected = (
            1057
            - np.cos(2 * phi)
            + 12 * (27 + np.cos(2 * phi)) * np.cos(varphi)
            - 2 * np.cos(2 * varphi) * np.sin(phi) * (16 * np.cos(phi) + 21 * np.sin(phi))
            + 16 * np.sin(2 * phi)
            - 8 * (-17 + np.cos(2 * phi) + 2 * np.sin(2 * phi)) * np.sin(varphi)
            - 8 * np.cos(2 * theta) * (3 + 3 * np.cos(varphi) + np.sin(varphi)) ** 2
            - 24 * np.cos(phi) * (np.cos(phi) + 2 * np.sin(phi)) * np.sin(2 * varphi)
            - 8
            * np.cos(theta)
            * (
                4
                * np.cos(phi)
                * (
                    4
                    + 8 * np.cos(varphi)
                    + np.cos(2 * varphi)
                    - (1 + 6 * np.cos(varphi)) * np.sin(varphi)
                )
                + np.sin(phi)
                * (
                    15
                    + 8 * np.cos(varphi)
                    - 11 * np.cos(2 * varphi)
                    + 42 * np.sin(varphi)
                    + 3 * np.sin(2 * varphi)
                )
            )
        ) / 16

        assert np.allclose(res, expected, atol=tol(dev.analytic))
