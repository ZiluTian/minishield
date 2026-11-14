# E20 prep: CFI metadata evidence from .v3ref (read-only)

## .v3ref/cfi contents
cfi_debug
cfi_debug.c
cfi_debug_nocfi
cfi_pipe
cfi_pipe.c
cfi_pipe_nocfi
cfi_pipe_nopie
cfi_pipe.s
demo
demo0
demo1
demo_lookup.c
demo_lookup.o
demo_main0.c
demo_main1.c
demo_main.c
demo_run.c
extlookup.c
extlookup.ll
extlookup.o
extlookup.s
good.cpp
good.ll
good.lto.o
good.o
good.s
icall_before.ll
icall_before.o
icall.c
icall.ll
icall.o
icall.s
lesson_icall_after.ll
lesson_icall_before.ll
lesson_vcall_after.ll
vcall_pipe
vcall_pipe.cpp
vcall_pipe.s
vcall_pre.ll
vcall_pre.o

## type.test metadata in cfi_pipe.s
53:  %20 = call i1 @llvm.type.test(ptr %19, metadata !"_ZTSFiiE"), !nosanitize !31
88:declare i1 @llvm.type.test(ptr, metadata) #5
120:!5 = !{i32 4, !"CFI Canonical Jump Tables", i32 1}
132:!17 = !{i64 0, !"_ZTSFiiE"}
133:!18 = !{i64 0, !"_ZTSFiiE.generalized"}

## type.test metadata in vcall_pipe.s
26:$_ZTS4Base = comdat any
44:@_ZTI4Base = linkonce_odr hidden constant { ptr, ptr } { ptr getelementptr inbounds (ptr, ptr @_ZTVN10__cxxabiv117__class_type_infoE, i64 2), ptr @_ZTS4Base }, comdat, align 8, !guid !17
46:@_ZTS4Base = linkonce_odr hidden constant [6 x i8] c"4Base\00", comdat, align 1, !guid !18
91:  %26 = call i1 @llvm.type.test(ptr %25, metadata !"_ZTS4Base"), !nosanitize !41
137:declare i1 @llvm.type.test(ptr, metadata) #7
187:!2 = !{i64 16, !"_ZTS4Base"}
188:!3 = !{i64 16, !"_ZTSM4BaseFiiE.virtual"}
190:!5 = !{i64 16, !"_ZTSM7DerivedFiiE.virtual"}
195:!10 = !{i64 16, !"_ZTSM4EvilFiiE.virtual"}
238:^5 = gv: (name: "_ZTS4Base", summaries: (variable: (module: ^0, flags: (linkage: linkonce_odr, visibility: hidden, notEligibleToImport: 1, live: 0, dsoLocal: 1, canAutoHide: 0, importType: definition, noRenameOnPromotion: 0), varFlags: (readonly: 0, writeonly: 0, constant: 1)))) ; guid = 2370067920813235120

## .cfi thunks (LTO copies carrying descriptors)
