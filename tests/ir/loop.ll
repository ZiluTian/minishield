define i32 @count_to(i32 %limit) {
entry:
  br label %header
header:
  %i = phi i32 [ 0, %entry ], [ %next, %body ]
  %continue = icmp slt i32 %i, %limit
  br i1 %continue, label %body, label %exit
body:
  %next = add i32 %i, 1
  br label %header
exit:
  ret i32 %i
}
