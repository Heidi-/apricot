import scipy
import numpy

try:
	import cupy
except:
	import numpy as cupy

from apricot import MaxCoverageSelection
from apricot.optimizers import *

from sklearn.datasets import load_digits
from sklearn.metrics import pairwise_distances

from numpy.testing import assert_almost_equal
from numpy.testing import assert_array_equal
from numpy.testing import assert_array_almost_equal

#print("[" + ", ".join(map(str, model.ranking)) + "]")
#print("[" + ", ".join([str(round(gain, 4)) for gain in model.gains]) + "]")

numpy.random.seed(0)
X_digits = numpy.random.choice(2, size=(300, 1000), p=[0.99, 0.01])
X_digits = numpy.array(X_digits, dtype='float64')

X_digits_sparse = scipy.sparse.csr_matrix(X_digits)
X_digits_cupy = cupy.array(X_digits)

digits_ranking = [135, 260, 89, 168, 203, 6, 62, 139, 86, 274, 78, 146, 
	138, 158, 193, 60, 71, 77, 256, 184, 23, 125, 155, 194, 280, 93, 212, 
	167, 201, 206, 38, 26, 101, 64, 11, 162, 225, 49, 50, 289, 103, 254, 7, 
	21, 227, 178, 81, 127, 161, 174, 186, 177, 107, 271, 121, 251, 236, 279, 
	272, 37, 252, 102, 219, 229, 283, 133, 207, 73, 43, 297, 273, 85, 137, 
	263, 74, 87, 96, 32, 134, 36, 31, 149, 287, 169, 209, 30, 24, 152, 10, 
	117, 241, 222, 284, 240, 141, 218, 136, 235, 269, 270]

digits_gains = [20.0, 19.0, 18.0, 17.0, 17.0, 16.0, 16.0, 16.0, 15.0, 15.0, 
	14.0, 14.0, 13.0, 13.0, 13.0, 12.0, 12.0, 12.0, 12.0, 12.0, 11.0, 11.0, 
	11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0, 9.0, 9.0, 9.0, 
	9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 7.0, 
	7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 
	6.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 
	5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 
	3.0, 3.0, 3.0, 3.0, 3.0]

digits_greedi_ranking = [135, 260, 276, 89, 62, 6, 203, 274, 280, 56, 139, 
	78, 193, 71, 138, 176, 158, 23, 178, 251, 243, 206, 153, 225, 15, 282, 
	184, 125, 162, 18, 38, 167, 41, 270, 160, 201, 279, 9, 145, 209, 73, 
	106, 70, 66, 241, 207, 155, 186, 11, 68, 214, 179, 254, 236, 90, 114, 
	219, 177, 127, 85, 228, 148, 107, 250, 143, 31, 194, 26, 227, 133, 287, 
	67, 208, 271, 233, 146, 297, 161, 24, 229, 272, 3, 21, 275, 108, 130, 
	277, 284, 121, 27, 40, 87, 97, 29, 291, 256, 190, 217, 75, 10]

digits_greedi_gains = [20.0, 19.0, 18.0, 17.0, 16.0, 16.0, 16.0, 15.0, 15.0, 
	14.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 12.0, 12.0, 11.0, 11.0, 
	11.0, 11.0, 11.0, 11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0, 
	9.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 
	7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 
	6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 5.0, 
	5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 
	4.0, 4.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]

digits_approx_ranking = [135, 260, 89, 168, 203, 6, 139, 62, 86, 78, 274, 
	146, 15, 60, 71, 178, 193, 280, 138, 158, 184, 125, 194, 207, 77, 251, 
	23, 206, 282, 7, 26, 162, 18, 41, 64, 167, 201, 212, 9, 38, 103, 224, 
	279, 236, 272, 56, 127, 283, 81, 248, 141, 179, 227, 155, 43, 133, 140, 
	174, 237, 241, 169, 177, 214, 172, 229, 252, 228, 161, 32, 240, 114, 69, 
	254, 112, 263, 244, 36, 11, 101, 122, 297, 98, 96, 21, 288, 117, 67, 108, 
	271, 292, 137, 31, 246, 149, 270, 275, 115, 87, 121, 218]

digits_approx_gains = [20.0, 19.0, 18.0, 17.0, 17.0, 16.0, 16.0, 16.0, 15.0, 
	14.0, 15.0, 14.0, 12.0, 12.0, 12.0, 12.0, 13.0, 12.0, 12.0, 13.0, 12.0, 
	11.0, 11.0, 11.0, 11.0, 10.0, 11.0, 10.0, 10.0, 10.0, 9.0, 10.0, 9.0, 9.0, 
	9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 
	7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 
	6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 
	4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 
	4.0, 4.0, 3.0, 3.0, 3.0, 3.0]

digits_stochastic_ranking = [208, 149, 145, 285, 205, 124, 48, 160, 161, 179, 
	248, 200, 84, 284, 78, 183, 27, 79, 60, 19, 253, 83, 209, 281, 286, 94, 
	126, 8, 210, 180, 292, 25, 88, 41, 98, 172, 165, 58, 188, 224, 159, 153, 
	121, 207, 135, 270, 152, 251, 240, 191, 185, 44, 102, 50, 202, 157, 26, 
	173, 193, 247, 110, 9, 130, 263, 260, 182, 115, 17, 268, 294, 189, 24, 99, 
	250, 272, 86, 299, 101, 232, 132, 216, 227, 49, 37, 56, 269, 231, 54, 109, 
	258, 255, 241, 206, 221, 222, 4, 178, 236, 297, 244]

digits_stochastic_gains = [8.0, 7.0, 11.0, 8.0, 7.0, 7.0, 7.0, 12.0, 13.0, 11.0, 
	9.0, 4.0, 10.0, 11.0, 13.0, 7.0, 11.0, 8.0, 11.0, 10.0, 6.0, 9.0, 8.0, 5.0, 
	6.0, 7.0, 7.0, 2.0, 5.0, 11.0, 8.0, 4.0, 6.0, 9.0, 8.0, 8.0, 8.0, 6.0, 7.0, 
	8.0, 4.0, 8.0, 8.0, 11.0, 14.0, 8.0, 5.0, 7.0, 7.0, 8.0, 6.0, 3.0, 5.0, 6.0, 
	9.0, 2.0, 4.0, 5.0, 8.0, 4.0, 3.0, 5.0, 5.0, 4.0, 8.0, 6.0, 6.0, 5.0, 6.0, 
	2.0, 1.0, 4.0, 3.0, 8.0, 2.0, 10.0, 8.0, 4.0, 1.0, 7.0, 6.0, 5.0, 3.0, 5.0, 
	5.0, 3.0, 2.0, 1.0, 4.0, 0.0, 1.0, 4.0, 7.0, 1.0, 3.0, 2.0, 6.0, 8.0, 3.0, 
	5.0]

digits_sample_ranking = [135, 260, 89, 276, 203, 62, 6, 168, 280, 274, 139, 78, 
	193, 138, 158, 176, 146, 23, 71, 178, 38, 243, 251, 282, 287, 7, 18, 41, 
	167, 114, 75, 66, 217, 26, 254, 64, 115, 155, 207, 1, 279, 73, 11, 70, 106, 
	236, 9, 292, 51, 141, 227, 297, 148, 186, 21, 125, 36, 80, 219, 133, 209, 
	269, 85, 145, 179, 283, 107, 43, 271, 143, 86, 288, 29, 201, 153, 284, 241, 
	17, 156, 68, 31, 177, 32, 10, 56, 130, 137, 127, 67, 252, 214, 266, 197, 
	151, 291, 27, 14, 79, 150, 237]

digits_sample_gains = [20.0, 19.0, 18.0, 17.0, 16.0, 16.0, 16.0, 15.0, 14.0, 
	14.0, 14.0, 14.0, 13.0, 13.0, 13.0, 13.0, 12.0, 12.0, 12.0, 12.0, 11.0, 
	11.0, 11.0, 11.0, 11.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0, 9.0, 9.0, 
	9.0, 9.0, 9.0, 9.0, 9.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 7.0, 7.0, 7.0, 
	7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 
	6.0, 6.0, 6.0, 6.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 
	5.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0, 
	3.0, 3.0, 3.0, 3.0, 3.0, 3.0]

digits_modular_ranking = [135, 260, 276, 168, 89, 203, 139, 6, 274, 62, 214, 
	146, 280, 86, 38, 31, 138, 158, 246, 176, 78, 184, 207, 75, 23, 162, 56, 
	77, 206, 287, 106, 297, 71, 15, 236, 178, 60, 217, 161, 160, 282, 11, 169, 
	66, 256, 275, 18, 96, 68, 72, 272, 193, 227, 194, 225, 53, 179, 70, 125, 
	115, 201, 202, 212, 64, 186, 121, 83, 270, 101, 41, 141, 27, 261, 16, 97, 
	143, 153, 249, 196, 167, 284, 233, 10, 241, 87, 43, 269, 46, 180, 136, 
	134, 82, 85, 165, 116, 177, 145, 103, 133, 155]

digits_modular_gains = [20.0, 19.0, 18.0, 15.0, 17.0, 16.0, 14.0, 16.0, 14.0, 
	16.0, 11.0, 13.0, 13.0, 12.0, 12.0, 11.0, 13.0, 12.0, 10.0, 9.0, 13.0, 
	10.0, 11.0, 9.0, 11.0, 8.0, 7.0, 9.0, 10.0, 11.0, 8.0, 8.0, 8.0, 8.0, 8.0, 
	10.0, 8.0, 5.0, 7.0, 7.0, 10.0, 6.0, 8.0, 6.0, 7.0, 6.0, 8.0, 5.0, 6.0, 
	7.0, 3.0, 10.0, 6.0, 7.0, 9.0, 2.0, 6.0, 5.0, 7.0, 4.0, 6.0, 4.0, 5.0, 
	7.0, 4.0, 4.0, 6.0, 8.0, 4.0, 4.0, 6.0, 2.0, 5.0, 2.0, 6.0, 5.0, 3.0, 
	3.0, 2.0, 6.0, 1.0, 5.0, 6.0, 6.0, 4.0, 6.0, 2.0, 3.0, 2.0, 4.0, 3.0, 
	1.0, 5.0, 1.0, 5.0, 4.0, 3.0, 5.0, 4.0, 2.0]

# Test some concave functions

def test_digits_naive():
	return
	model = MaxCoverageSelection(100, optimizer='naive')
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_ranking)
	assert_array_equal(model.ranking, digits_ranking)
	assert_array_almost_equal(model.gains, digits_gains, 4)

def test_digits_lazy():
	model = MaxCoverageSelection(100, optimizer='lazy')
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:3], digits_ranking[:3])
	assert_array_almost_equal(model.gains[:3], digits_gains[:3], 4)

def test_digits_two_stage():
	model = MaxCoverageSelection(100, optimizer='two-stage')
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:3], digits_ranking[:3])
	assert_array_almost_equal(model.gains[:3], digits_gains[:3], 4)

# Test with initialization

def test_digits_naive_init():
	model = MaxCoverageSelection(100, optimizer='naive', 
		initial_subset=digits_ranking[:5])
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:10], digits_ranking[5:15])
	assert_array_almost_equal(model.gains[:10], digits_gains[5:15], 4)

def test_digits_lazy_init():
	model = MaxCoverageSelection(100, optimizer='lazy', 
		initial_subset=digits_ranking[:5])
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:5], digits_ranking[5:10])
	assert_array_almost_equal(model.gains[:5], digits_gains[5:10], 4)

def test_digits_two_stage_init():
	model = MaxCoverageSelection(100, optimizer='two-stage', 
		initial_subset=digits_ranking[:5])
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:10], digits_ranking[5:15])
	assert_array_almost_equal(model.gains[:10], digits_gains[5:15], 4)

# Test all optimizers

def test_digits_greedi_nn():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'naive', 'optimizer2': 'naive'}, 
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_greedi_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_greedi_gains[:2], 4)

def test_digits_greedi_ll():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'lazy', 'optimizer2': 'lazy'}, 
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:30], digits_greedi_ranking[:30])
	assert_array_almost_equal(model.gains[:30], digits_greedi_gains[:30], 4)

def test_digits_greedi_ln():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'lazy', 'optimizer2': 'naive'}, 
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_greedi_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_greedi_gains[:2], 4)

def test_digits_greedi_nl():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'naive', 'optimizer2': 'lazy'}, 
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_greedi_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_greedi_gains[:2], 4)

def test_digits_approximate():
	model = MaxCoverageSelection(100, optimizer='approximate-lazy')
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_approx_ranking)
	assert_array_almost_equal(model.gains, digits_approx_gains, 4)

def test_digits_stochastic():
	model = MaxCoverageSelection(100, optimizer='stochastic',
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_stochastic_ranking)
	assert_array_almost_equal(model.gains, digits_stochastic_gains, 4)

def test_digits_sample():
	model = MaxCoverageSelection(100, optimizer='sample',
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_sample_ranking)
	assert_array_almost_equal(model.gains, digits_sample_gains, 4)

def test_digits_modular():
	model = MaxCoverageSelection(100, optimizer='modular',
		random_state=0)
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_modular_ranking)
	assert_array_almost_equal(model.gains, digits_modular_gains, 4)


# Using Optimizer Objects

def test_digits_naive_object():
	model = MaxCoverageSelection(100, optimizer=NaiveGreedy())
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:4], digits_ranking[:4])
	assert_array_almost_equal(model.gains[:4], digits_gains[:4], 4)

def test_digits_lazy_object():
	model = MaxCoverageSelection(100, optimizer=LazyGreedy())
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:3], digits_ranking[:3])
	assert_array_almost_equal(model.gains[:3], digits_gains[:3], 4)

def test_digits_two_stage_object():
	model = MaxCoverageSelection(100, optimizer=TwoStageGreedy())
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:4], digits_ranking[:4])
	assert_array_almost_equal(model.gains[:4], digits_gains[:4], 4)

def test_digits_greedi_nn_object():
	model = MaxCoverageSelection(100, optimizer=GreeDi(
		optimizer1='naive', optimizer2='naive', random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_greedi_ll_object():
	model = MaxCoverageSelection(100, optimizer=GreeDi(
		optimizer1='lazy', optimizer2='lazy', random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_greedi_ln_object():
	model = MaxCoverageSelection(100, optimizer=GreeDi(
		optimizer1='lazy', optimizer2='naive', random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_greedi_nl_object():
	model = MaxCoverageSelection(100, optimizer=GreeDi(
		optimizer1='naive', optimizer2='lazy', random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_approximate_object():
	model = MaxCoverageSelection(100, 
		optimizer=ApproximateLazyGreedy())
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_approx_ranking)
	assert_array_almost_equal(model.gains, digits_approx_gains, 4)

def test_digits_stochastic_object():
	model = MaxCoverageSelection(100, 
		optimizer=StochasticGreedy(random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_stochastic_ranking)
	assert_array_almost_equal(model.gains, digits_stochastic_gains, 4)

def test_digits_sample_object():
	model = MaxCoverageSelection(100, 
		optimizer=SampleGreedy(random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_sample_ranking)
	assert_array_almost_equal(model.gains, digits_sample_gains, 4)

def test_digits_modular_object():
	model = MaxCoverageSelection(100, 
		optimizer=ModularGreedy(random_state=0))
	model.fit(X_digits_cupy)
	assert_array_equal(model.ranking, digits_modular_ranking)
	assert_array_almost_equal(model.gains, digits_modular_gains, 4)

# Test all optimizers on sparse data

def test_digits_naive_sparse():
	model = MaxCoverageSelection(100, optimizer='naive')
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:4], digits_ranking[:4])
	assert_array_almost_equal(model.gains[:4], digits_gains[:4], 4)

def test_digits_lazy_sparse():
	model = MaxCoverageSelection(100, optimizer='lazy')
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:3], digits_ranking[:3])
	assert_array_almost_equal(model.gains[:3], digits_gains[:3], 4)

def test_digits_two_stage_sparse():
	model = MaxCoverageSelection(100, optimizer='two-stage')
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:4], digits_ranking[:4])
	assert_array_almost_equal(model.gains[:4], digits_gains[:4], 4)

def test_digits_greedi_nn_sparse():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'naive', 'optimizer2': 'naive'}, 
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_greedi_ll_sparse():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'lazy', 'optimizer2': 'lazy'}, 
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_greedi_ln_sparse():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'lazy', 'optimizer2': 'naive'}, 
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_greedi_nl_sparse():
	model = MaxCoverageSelection(100, optimizer='greedi',
		optimizer_kwds={'optimizer1': 'naive', 'optimizer2': 'lazy'}, 
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking[:2], digits_ranking[:2])
	assert_array_almost_equal(model.gains[:2], digits_gains[:2], 4)

def test_digits_approximate_sparse():
	model = MaxCoverageSelection(100, optimizer='approximate-lazy')
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking, digits_approx_ranking)
	assert_array_almost_equal(model.gains, digits_approx_gains, 4)

def test_digits_stochastic_sparse():
	model = MaxCoverageSelection(100, optimizer='stochastic',
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking, digits_stochastic_ranking)
	assert_array_almost_equal(model.gains, digits_stochastic_gains, 4)

def test_digits_sample():
	model = MaxCoverageSelection(100, optimizer='sample',
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking, digits_sample_ranking)
	assert_array_almost_equal(model.gains, digits_sample_gains, 4)

def test_digits_modular():
	model = MaxCoverageSelection(100, optimizer='modular',
		random_state=0)
	model.fit(X_digits_sparse)
	assert_array_equal(model.ranking, digits_modular_ranking)
	assert_array_almost_equal(model.gains, digits_modular_gains, 4)
