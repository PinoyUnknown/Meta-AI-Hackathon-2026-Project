/**
 * Meta Model Integration & Invariant Test Suite
 * Automated tests for ML developers, testers, and CI/CD validation
 */

import { metaModelService } from '../src/services/metaModelApi.js';
import { DOMAIN_PRESETS } from '../src/services/domainData.js';

async function runAllTests() {
  console.log('\x1b[36m========================================================\x1b[0m');
  console.log('\x1b[36m   MetaFrontier NeuroTwin - Model QA & Invariant Tests  \x1b[0m');
  console.log('\x1b[36m========================================================\x1b[0m\n');

  let passed = 0;
  let failed = 0;

  // Test 1: Domain Presets Integrity
  console.log('Test 1: Validating Domain Presets & Telemetry Data...');
  const expectedDomains = ['robotics', 'biomedical', 'energy', 'microelectronics'];
  let domainsValid = true;
  for (const d of expectedDomains) {
    if (!DOMAIN_PRESETS[d] || DOMAIN_PRESETS[d].targets.length === 0) {
      domainsValid = false;
      break;
    }
  }
  if (domainsValid) {
    console.log('  \x1b[32m✔ PASS\x1b[0m: All 4 frontier domains loaded with targets and equations.\n');
    passed++;
  } else {
    console.log('  \x1b[31m✖ FAIL\x1b[0m: Missing domain presets.\n');
    failed++;
  }

  // Test 2: SAM 3.1 Segmentation Simulation
  console.log('Test 2: Validating SAM 3.1 Point-Prompt Spatial Inference...');
  try {
    const samResult = await metaModelService.runSAMSegmentation('robotics', [[380, 260]]);
    if (samResult.status === 'success' && samResult.polygon.length > 3 && samResult.iouScore > 0.9) {
      console.log(`  \x1b[32m✔ PASS\x1b[0m: SAM 3.1 segmented ${samResult.target.name} with IoU ${(samResult.iouScore * 100).toFixed(1)}%.\n`);
      passed++;
    } else {
      console.log('  \x1b[31m✖ FAIL\x1b[0m: SAM 3.1 returned invalid geometry.\n');
      failed++;
    }
  } catch (err) {
    console.log(`  \x1b[31m✖ FAIL\x1b[0m: SAM 3.1 execution error: ${err.message}\n`);
    failed++;
  }

  // Test 3: Multi-Agent Reasoning Chain Stream
  console.log('Test 3: Validating Multi-Agent Chain-of-Thought Stream...');
  try {
    const steps = [];
    for await (const step of metaModelService.streamMultiAgentReasoning('robotics')) {
      steps.push(step);
    }
    if (steps.length === 4) {
      console.log(`  \x1b[32m✔ PASS\x1b[0m: All 4 agents (Perception, Physics, Muse Code, QA) completed successfully.\n`);
      passed++;
    } else {
      console.log(`  \x1b[31m✖ FAIL\x1b[0m: Expected 4 agent steps, got ${steps.length}.\n`);
      failed++;
    }
  } catch (err) {
    console.log(`  \x1b[31m✖ FAIL\x1b[0m: Agent stream error: ${err.message}\n`);
    failed++;
  }

  // Test 4: Benchmark Matrix Health
  console.log('Test 4: Validating Benchmark Matrix Execution...');
  try {
    const bench = await metaModelService.runModelBenchmarks();
    if (bench.status === 'OPTIMAL' && bench.models.length === 4) {
      console.log(`  \x1b[32m✔ PASS\x1b[0m: Evaluated ${bench.models.length} Meta models. Score: ${bench.overallBenchmarkScore}.\n`);
      passed++;
    } else {
      console.log('  \x1b[31m✖ FAIL\x1b[0m: Benchmark scorecard incomplete.\n');
      failed++;
    }
  } catch (err) {
    console.log(`  \x1b[31m✖ FAIL\x1b[0m: Benchmark error: ${err.message}\n`);
    failed++;
  }

  // Final Summary
  console.log('\x1b[36m--------------------------------------------------------\x1b[0m');
  console.log(`Summary: ${passed} passed, ${failed} failed.`);
  if (failed === 0) {
    console.log('\x1b[1m\x1b[32mALL TESTS PASSED! Project is ready for Hackathon presentation.\x1b[0m\n');
  } else {
    process.exit(1);
  }
}

runAllTests();
