declare i32 @callee()
declare i32 @__gxx_personality_v0(...)

define i32 @with_invoke() personality ptr @__gxx_personality_v0 {
entry:
  %result = invoke i32 @callee() to label %normal unwind label %exception
normal:
  ret i32 %result
exception:
  %landing = landingpad { ptr, i32 } cleanup
  resume { ptr, i32 } %landing
}

define void @with_indirectbr(i1 %condition) {
entry:
  %target = select i1 %condition,
    ptr blockaddress(@with_indirectbr, %left),
    ptr blockaddress(@with_indirectbr, %right)
  indirectbr ptr %target, [label %left, label %right]
left:
  ret void
right:
  ret void
}

; A read-only inspection pass should run even when optimization is disabled.
define void @without_optimization() noinline optnone {
entry:
  ret void
}
