define i32 @choose(i1 %condition) {
entry:
  br i1 %condition, label %yes, label %no
yes:
  ret i32 1
no:
  ret i32 0
}
