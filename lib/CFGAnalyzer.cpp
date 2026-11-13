// Copyright (c) 2026 ZiluTian
//
// MiniShield code is licensed under MIT; see LICENSE.
// The MiniShield books (day1, day2, day3, docs/, PLAN.md) are CC BY-NC 4.0.
#include "minishield/CFGAnalyzer.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Dominators.h"
#include "llvm/Analysis/LoopInfo.h"

namespace minishield {
    llvm::AnalysisKey CFGAnalyzer::Key;
    CFGAnalyzer::Result CFGAnalyzer::run(llvm::Function &F, llvm::FunctionAnalysisManager &AM) {
        Result result{};
        const auto &DT = AM.getResult<llvm::DominatorTreeAnalysis>(F);
        const auto &LI = AM.getResult<llvm::LoopAnalysis>(F);
        result.loopCount = LI.getLoopsInPreorder().size();

        for (const llvm::BasicBlock &BB : F){
            BlockInfo info{};
            info.block = &BB;
            info.terminatorOpcode = BB.getTerminator()->getOpcode();
            for (const llvm::BasicBlock *successor : llvm::successors(&BB)) {
                info.successors.push_back(successor);
                if (DT.isReachableFromEntry(&BB) && (DT.dominates(successor, &BB))) {
                   result.backEdges.push_back({&BB, successor}); 
                }
            }
            for (const llvm::BasicBlock *predecessor: llvm::predecessors(&BB)) {
                info.predecessors.push_back(predecessor);
            }
            result.blocks.push_back(info);
        }
        return result;
    }
} // namespace minishield
