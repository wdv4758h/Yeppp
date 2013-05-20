using System.Runtime.InteropServices;

namespace Yeppp
{

	public class Core
	{
		public static unsafe double DotProduct_V64fV64f_S64f(double[] xArray, int xOffset, double[] yArray, int yOffset, int length) {
			fixed (double* xPointer = &xArray[xOffset])
			fixed (double* yPointer = &yArray[yOffset])
				return DotProduct_V64fV64f_S64f(xPointer, yPointer, length);
		}

		public static unsafe double DotProduct_V64fV64f_S64f(double* xPointer, double* yPointer, int length) {
			double z;
			yepCore_DotProduct_V64fV64f_S64f(xPointer, yPointer, out z, new System.UIntPtr(unchecked((uint) length)));
			return z;
		}

		public static unsafe double SumSquares_V64f_S64f(double[] xArray, int xOffset, int length) {
			fixed (double* xPointer = &xArray[xOffset])
				return SumSquares_V64f_S64f(xPointer, length);
		}

		public static unsafe double SumSquares_V64f_S64f(double* xPointer, int length) {
			double s;
			yepCore_SumSquares_V64f_S64f(xPointer, out s, new System.UIntPtr(unchecked((uint) length)));
			return s;
		}

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepCore_DotProduct_V64fV64f_S64f")]
		private static unsafe extern Status yepCore_DotProduct_V64fV64f_S64f(double* xPointer, double* yPointer, out double z, System.UIntPtr length);

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepCore_SumSquares_V64f_S64f")]
		private static unsafe extern Status yepCore_SumSquares_V64f_S64f(double* xPointer, out double s, System.UIntPtr length);
	}

}
