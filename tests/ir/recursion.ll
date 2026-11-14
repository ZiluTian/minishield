define i32 @factorial(i32 %n) {
entry:
  %base = icmp sle i32 %n, 1
  br i1 %base, label %done, label %recurse
done:
  ret i32 1
recurse:
  %previous = sub i32 %n, 1
  %partial = call i32 @factorial(i32 %previous)
  %result = mul i32 %n, %partial
  ret i32 %result
}
