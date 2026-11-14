// Copyright (c) 2026 ZiluTian
//
// MiniShield code is licensed under MIT; see LICENSE.
// The MiniShield books (day1, day2, day3, docs/, PLAN.md) are CC BY-NC 4.0.
#include "minishield/FlatteningPass.h"
#include "minishield/FunctionEligibility.h"

#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
namespace minishield {

llvm::PreservedAnalyses FlatteningPass::run(
    llvm::Function &F,
    llvm::FunctionAnalysisManager &AM){
    if (F.isDeclaration())
        return llvm::PreservedAnalyses::all();
    
    const auto eligibility = FunctionEligibility::check(F);
    if (!eligibility.eligible) {
        llvm::errs() << "[MiniShield] rejected: " << F.getName() << ": " << eligibility.reason << "\n";
        return llvm::PreservedAnalyses::all();
    }

    llvm::errs() << "[MiniShield] eligible: " << F.getName() << "\n";

    return llvm::PreservedAnalyses::all();
}
} // namespace minishield
