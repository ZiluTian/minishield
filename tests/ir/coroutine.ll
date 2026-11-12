declare ptr @llvm.coro.noop()

define ptr @coroutine_handle() {
entry:
	%handle = call ptr @llvm.coro.noop()
	ret ptr %handle
}
