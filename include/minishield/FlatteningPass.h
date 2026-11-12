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

