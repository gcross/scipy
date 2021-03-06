# Copyright (C) 2003-2005 Peter J. Verveer
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#
# 3. The name of the author may not be used to endorse or promote
#    products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import types
import numpy
import _ni_support
import _nd_image

__all__ = ['fourier_gaussian', 'fourier_uniform', 'fourier_ellipsoid',
           'fourier_shift']


def _get_output_fourier(output, input):
    if output is None:
        if input.dtype.type in [numpy.complex64, numpy.complex128,
                                numpy.float32]:
            output = numpy.zeros(input.shape, dtype = input.dtype)
        else:
            output = numpy.zeros(input.shape, dtype = numpy.float64)
        return_value = output
    elif type(output) is types.TypeType:
        if output not in [numpy.complex64, numpy.complex128,
                          numpy.float32, numpy.float64]:
            raise RuntimeError("output type not supported")
        output = numpy.zeros(input.shape, dtype = output)
        return_value = output
    else:
        if output.shape != input.shape:
            raise RuntimeError("output shape not correct")
        return_value = None
    return output, return_value

def _get_output_fourier_complex(output, input):
    if output is None:
        if input.dtype.type in [numpy.complex64, numpy.complex128]:
            output = numpy.zeros(input.shape, dtype = input.dtype)
        else:
            output = numpy.zeros(input.shape, dtype = numpy.complex128)
        return_value = output
    elif type(output) is types.TypeType:
        if output not in [numpy.complex64, numpy.complex128]:
            raise RuntimeError("output type not supported")
        output = numpy.zeros(input.shape, dtype = output)
        return_value = output
    else:
        if output.shape != input.shape:
            raise RuntimeError("output shape not correct")
        return_value = None
    return output, return_value

def fourier_gaussian(input, sigma, n = -1, axis = -1, output = None):
    """
    Multi-dimensional Gaussian fourier filter.

    The array is multiplied with the fourier transform of a Gaussian
    kernel.

    Parameters
    ----------
    input : array_like
        The input array.
    sigma : float or sequence
        The sigma of the Gaussian kernel. If a float, `sigma` is the same for
        all axes. If a sequence, `sigma` has to contain one value for each
        axis.
    n : int, optional
        If `n` is negative (default), then the input is assumed to be the
        result of a complex fft.
        If `n` is larger than or equal to zero, the input is assumed to be the
        result of a real fft, and `n` gives the length of the array before
        transformation along the real transform direction.
    axis : int, optional
        The axis of the real transform.
    output : ndarray, optional
        If given, the result of filtering the input is placed in this array.
        None is returned in this case.

    Returns
    -------
    return_value : ndarray or None
        The filtered input. If `output` is given as a parameter, None is
        returned.

    """
    input = numpy.asarray(input)
    output, return_value = _get_output_fourier(output, input)
    axis = _ni_support._check_axis(axis, input.ndim)
    sigmas = _ni_support._normalize_sequence(sigma, input.ndim)
    sigmas = numpy.asarray(sigmas, dtype = numpy.float64)
    if not sigmas.flags.contiguous:
        sigmas = sigmas.copy()

    _nd_image.fourier_filter(input, sigmas, n, axis, output, 0)
    return return_value

def fourier_uniform(input, size, n = -1, axis = -1, output = None):
    """
    Multi-dimensional uniform fourier filter.

    The array is multiplied with the fourier transform of a box of given
    size.

    Parameters
    ----------
    input : array_like
        The input array.
    size : float or sequence
        The size of the box used for filtering.
        If a float, `size` is the same for all axes. If a sequence, `size` has
        to contain one value for each axis.
    n : int, optional
        If `n` is negative (default), then the input is assumed to be the
        result of a complex fft.
        If `n` is larger than or equal to zero, the input is assumed to be the
        result of a real fft, and `n` gives the length of the array before
        transformation along the real transform direction.
    axis : int, optional
        The axis of the real transform.
    output : ndarray, optional
        If given, the result of filtering the input is placed in this array.
        None is returned in this case.

    Returns
    -------
    return_value : ndarray or None
        The filtered input. If `output` is given as a parameter, None is
        returned.

    """
    input = numpy.asarray(input)
    output, return_value = _get_output_fourier(output, input)
    axis = _ni_support._check_axis(axis, input.ndim)
    sizes = _ni_support._normalize_sequence(size, input.ndim)
    sizes = numpy.asarray(sizes, dtype = numpy.float64)
    if not sizes.flags.contiguous:
        sizes = sizes.copy()
    _nd_image.fourier_filter(input, sizes, n, axis, output, 1)
    return return_value

def fourier_ellipsoid(input, size, n = -1, axis = -1, output = None):
    """
    Multi-dimensional ellipsoid fourier filter.

    The array is multiplied with the fourier transform of a ellipsoid of
    given sizes.

    Parameters
    ----------
    input : array_like
        The input array.
    size : float or sequence
        The size of the box used for filtering.
        If a float, `size` is the same for all axes. If a sequence, `size` has
        to contain one value for each axis.
    n : int, optional
        If `n` is negative (default), then the input is assumed to be the
        result of a complex fft.
        If `n` is larger than or equal to zero, the input is assumed to be the
        result of a real fft, and `n` gives the length of the array before
        transformation along the real transform direction.
    axis : int, optional
        The axis of the real transform.
    output : ndarray, optional
        If given, the result of filtering the input is placed in this array.
        None is returned in this case.

    Returns
    -------
    return_value : ndarray or None
        The filtered input. If `output` is given as a parameter, None is
        returned.

    Notes
    -----
    This function is implemented for arrays of rank 1, 2, or 3.

    """
    input = numpy.asarray(input)
    output, return_value = _get_output_fourier(output, input)
    axis = _ni_support._check_axis(axis, input.ndim)
    sizes = _ni_support._normalize_sequence(size, input.ndim)
    sizes = numpy.asarray(sizes, dtype = numpy.float64)
    if not sizes.flags.contiguous:
        sizes = sizes.copy()
    _nd_image.fourier_filter(input, sizes, n, axis, output, 2)
    return return_value

def fourier_shift(input, shift, n = -1, axis = -1, output = None):
    """
    Multi-dimensional fourier shift filter.

    The array is multiplied with the fourier transform of a shift operation.

    Parameters
    ----------
    input : array_like
        The input array.
    shift : float or sequence
        The size of the box used for filtering.
        If a float, `shift` is the same for all axes. If a sequence, `shift`
        has to contain one value for each axis.
    n : int, optional
        If `n` is negative (default), then the input is assumed to be the
        result of a complex fft.
        If `n` is larger than or equal to zero, the input is assumed to be the
        result of a real fft, and `n` gives the length of the array before
        transformation along the real transform direction.
    axis : int, optional
        The axis of the real transform.
    output : ndarray, optional
        If given, the result of shifting the input is placed in this array.
        None is returned in this case.

    Returns
    -------
    return_value : ndarray or None
        The shifted input. If `output` is given as a parameter, None is
        returned.

    """
    input = numpy.asarray(input)
    output, return_value = _get_output_fourier_complex(output, input)
    axis = _ni_support._check_axis(axis, input.ndim)
    shifts = _ni_support._normalize_sequence(shift, input.ndim)
    shifts = numpy.asarray(shifts, dtype = numpy.float64)
    if not shifts.flags.contiguous:
        shifts = shifts.copy()
    _nd_image.fourier_shift(input, shifts, n, axis, output)
    return return_value
