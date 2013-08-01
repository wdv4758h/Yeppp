using System.Runtime.InteropServices;

namespace Yeppp
{

	internal enum Status {
		Ok = 0,
		NullPointer = 1,
		MisalignedPointer = 2,
		InvalidArgument = 3,
		InvalidData = 4,
		InvalidState = 5,
		UnsupportedHardware = 6,
		UnsupportedSoftware = 7,
		InsufficientBuffer = 8,
		OutOfMemory = 9,
		SystemError = 10
	}

	public class Library
	{
		internal static void Init()
		{
			Status status = yepLibrary_Init();
			if (status != Status.Ok) {
				throw new System.SystemException();
			}
		}

		public static void Release()
		{
			Status status = yepLibrary_Release();
			if (status != Status.Ok) {
				throw new System.SystemException();
			}
		}
		
		public static ulong GetTimerTicks()
		{
			ulong ticks;
			Status status = yepLibrary_GetTimerTicks(out ticks);
			if (status != Status.Ok) {
				throw new System.SystemException();
			}
			return ticks;
		}

		public static ulong GetTimerFrequency()
		{
			ulong frequency;
			Status status = yepLibrary_GetTimerFrequency(out frequency);
			if (status != Status.Ok) {
				throw new System.SystemException();
			}
			return frequency;
		}

		public static ulong GetTimerAccuracy()
		{
			ulong accuracy;
			Status status = yepLibrary_GetTimerAccuracy(out accuracy);
			if (status != Status.Ok) {
				throw new System.SystemException();
			}
			return accuracy;
		}

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepLibrary_Init")]
		private static extern Status yepLibrary_Init();

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepLibrary_Release")]
		private static extern Status yepLibrary_Release();

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepLibrary_GetTimerTicks")]
		private static extern Status yepLibrary_GetTimerTicks(out ulong ticks);

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepLibrary_GetTimerFrequency")]
		private static extern Status yepLibrary_GetTimerFrequency(out ulong frequency);

		[DllImport("yeppp", ExactSpelling=true, CallingConvention=CallingConvention.Cdecl, EntryPoint="yepLibrary_GetTimerAccuracy")]
		private static extern Status yepLibrary_GetTimerAccuracy(out ulong accuracy);
	}

}
