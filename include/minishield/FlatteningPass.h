// Copyright (c) 2026 ZiluTian
//
// MiniShield code is licensed under MIT; see LICENSE.
// The MiniShield books (day1, day2, day3, docs/, PLAN.md) are CC BY-NC 4.0.
#pragma once
#include "llvm/IR/PassManager.h"

namespace minishield {
    class FlatteningPass : public llvm::OptionalPassInfoMixin<FlatteningPass> {
        public:
            llvm::PreservedAnalyses run(
                    llvm::Function &F,
                    llvm::FunctionAnalysisManager &AM);
    };
} // namespace minishield

