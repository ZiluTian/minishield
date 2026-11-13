// Copyright (c) 2026 ZiluTian
//
// MiniShield code is licensed under MIT; see LICENSE.
// The MiniShield books (volume1, volume2, volume3, docs/, PLAN.md) are CC BY-NC 4.0.
#pragma once
#include "llvm/IR/PassManager.h"

namespace minishield {
    class StatsPass : public llvm::RequiredPassInfoMixin<StatsPass> {
        public:
            llvm::PreservedAnalyses run(
                    llvm::Function &F,
                    llvm::FunctionAnalysisManager &AM);
    };
} // namespace minishield

