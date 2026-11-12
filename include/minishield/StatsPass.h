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

