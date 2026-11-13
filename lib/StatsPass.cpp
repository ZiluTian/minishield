// Copyright (c) 2026 ZiluTian
//
// MiniShield code is licensed under MIT; see LICENSE.
// The MiniShield books (day1, day2, day3, docs/, PLAN.md) are CC BY-NC 4.0.
#include "minishield/StatsPass.h"
#include "minishield/CFGAnalyzer.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Instructions.h"
#include "llvm/Support/Casting.h"

namespace minishield {

llvm::PreservedAnalyses StatsPass::run(
    llvm::Function &F,
    llvm::FunctionAnalysisManager &AM){
    
    if (F.isDeclaration())
        return llvm::PreservedAnalyses::all();

    const auto &cfg = AM.getResult<CFGAnalyzer>(F);

    for (const auto &pair : cfg.backEdges) {
        llvm::errs() << pair.source->getName() << " -> " << pair.target->getName() << "\n";    
    }

    llvm::errs() << "loops: " << cfg.loopCount;
    llvm::errs() << ", backedges: " << cfg.backEdges.size();
    llvm::errs() << "\n";

    for (const auto &info : cfg.blocks) {
        llvm::errs() << info.block->getName() << "| successors";
        for (const auto *successor : info.successors)
            llvm::errs() << " " << successor->getName();
        llvm::errs() << " | predecessors:";
        for (const auto *predecessor : info.predecessors)
            llvm::errs() << " " << predecessor->getName();
        llvm::errs() << " | terminators:";
        llvm::errs() << llvm::Instruction::getOpcodeName(info.terminatorOpcode);
        llvm::errs() << "\n";
    }

    int cond_br = 0, uncond_br = 0, calls=0, total_inst = 0, switches = 0, phis = 0, returns = 0, invokes = 0, indirectBranches = 0;

    for (const llvm::BasicBlock &BB : F) {
        for (const llvm::Instruction &I : BB) {
            ++total_inst;
            switch (I.getOpcode()) {
                case llvm::Instruction::CondBr:
                    ++cond_br;
                    break;
                case llvm::Instruction::UncondBr:
                    ++uncond_br;
                    break;
                case llvm::Instruction::Switch:
                    ++switches;
                    break;
                case llvm::Instruction::PHI:
                    ++phis;
                    break;
                case llvm::Instruction::Ret:
                    ++returns;
                    break;
                case llvm::Instruction::Call:
                    ++calls;
                    break;
                case llvm::Instruction::Invoke:
                    ++invokes;
                    break;
                case llvm::Instruction::IndirectBr:
                    ++indirectBranches;
                    break;
                default:
                    break;
            }
        }
    }
    llvm::errs() << "[MiniShield] function: " << F.getName()
        << ", blocks: " << F.size()
        << ", total instructions: " << total_inst
        << ", phi: " << phis
        << ", returns: "<< returns
        << ", switches: " << switches
        << ", calls: "<< calls
        << ", invokes: " << invokes
        << ", indirect branches: " << indirectBranches
        << ", conditional branches: " << cond_br
        << ", unconditional branches: " << uncond_br << "\n";
    return llvm::PreservedAnalyses::all();
}
} // namespace minishield
