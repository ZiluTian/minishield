#pragma once

#include "llvm/IR/PassManager.h"
#include "llvm/IR/BasicBlock.h"
#include <vector>

namespace minishield {
    class CFGAnalyzer : public llvm::AnalysisInfoMixin<CFGAnalyzer> {
        public:
        struct BlockInfo {
            const llvm::BasicBlock *block;
            std::vector<const llvm::BasicBlock *> successors;
            std::vector<const llvm::BasicBlock *> predecessors;      
            unsigned terminatorOpcode;
        };

        struct BackEdge {
            const llvm::BasicBlock *source;
            const llvm::BasicBlock *target;
        };

        struct Result {
            std::vector<BlockInfo> blocks;
            std::vector<BackEdge> backEdges;
            unsigned loopCount = 0;
        };

        Result run(llvm::Function &F, llvm::FunctionAnalysisManager &AM);

        private:
        friend llvm::AnalysisInfoMixin<CFGAnalyzer>;
        // Unique per analysis 
        static llvm::AnalysisKey Key;
    };
} // namespace minishield
