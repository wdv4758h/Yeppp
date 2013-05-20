using System.Runtime.InteropServices;

namespace Yeppp
{

	public class Math
	{
		public static unsafe void Log_V64f_V64f(double[] xArray, int xOffset, double[] yArray, int yOffset, int length) {
			fixed (double* xPointer = &xArray[xOffset])
			fixed (double* yPointer = &yArray[yOffset])
				yepMath_Log_V64f_V64f(xPointer, yPointer, new System.UIntPtr(unchecked((uint) length)));
		}

		public static unsafe void Log_V64f_V64f(double* xPointer, double* yPointer, int length) {
			yepMath_Log_V64f_V64f(xPointer, yPointer, new System.UIntPtr(unchecked((uint) length)));
		}

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepMath_Log_V64f_V64f")]
		private static unsafe extern Status yepMath_Log_V64f_V64f(double* xPointer, double* yPointer, System.UIntPtr length);
	}

}
