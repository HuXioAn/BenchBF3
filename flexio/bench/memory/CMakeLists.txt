project(FLEXIO_BENCH_MEMORY)

set(APP_ADDITIONAL_SOURCES)
file(GLOB FLEXIOSOURCES ${CMAKE_SOURCE_DIR}/wrapper_flexio/*.cpp)
list(APPEND APP_ADDITIONAL_SOURCES ${FLEXIOSOURCES})

set(app_dev_build_dir ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})
set(program_lib_include_dir "-I${CMAKE_SOURCE_DIR},-I${CMAKE_SOURCE_DIR}/wrapper_flexio,-I${CMAKE_CURRENT_SOURCE_DIR}")
set(program_user_lib)
set(dpacc_build_script ${CMAKE_SOURCE_DIR}/build_dpacc_samples.sh)

# bench_memory
set(memory_program_lib_name bench_memory_device)
set(memory_sample_name bench_memory)
set(memory_dev_source_file ${CMAKE_CURRENT_SOURCE_DIR}/device/bench_memory_device.c)
list(APPEND memory_dev_source_file ${CMAKE_SOURCE_DIR}/wrapper_flexio/wrapper_flexio_device.c)

add_executable(${memory_sample_name} ./bench_memory.cpp ${UTILSOURCES} ${APP_ADDITIONAL_SOURCES})
target_include_directories(${memory_sample_name} PRIVATE ${CMAKE_SOURCE_DIR})
target_compile_options(${memory_sample_name} PRIVATE -Wno-old-style-cast -Wno-maybe-uninitialized)

add_custom_command(OUTPUT dpacc_${memory_sample_name}
        COMMAND ${dpacc_build_script} ${memory_program_lib_name} \"${memory_dev_source_file}\" ${app_dev_build_dir} ${program_lib_include_dir} ${program_user_lib}
)
add_custom_target(
        dpacc_${memory_sample_name}_target ALL
        DEPENDS dpacc_${memory_sample_name}
)
add_dependencies(${memory_sample_name} dpacc_${memory_sample_name}_target)
target_link_libraries(${memory_sample_name} ${LIBRARIES} ${app_dev_build_dir}/${memory_program_lib_name}.a ibverbs mlx5)

# bench_cache
set(cache_program_lib_name bench_cache_device)
set(cache_sample_name bench_cache)
set(cache_dev_source_file ${CMAKE_CURRENT_SOURCE_DIR}/device/bench_cache_device.c)
list(APPEND cache_dev_source_file ${CMAKE_SOURCE_DIR}/wrapper_flexio/wrapper_flexio_device.c)

add_executable(${cache_sample_name} ./bench_cache.cpp ${UTILSOURCES} ${APP_ADDITIONAL_SOURCES})
target_include_directories(${cache_sample_name} PRIVATE ${CMAKE_SOURCE_DIR})
target_compile_definitions(${cache_sample_name} PRIVATE RUN_IN_DPA)
target_compile_options(${cache_sample_name} PRIVATE -Wno-old-style-cast -Wno-maybe-uninitialized)

add_custom_command(OUTPUT dpacc_${cache_sample_name}
        COMMAND ${dpacc_build_script} ${cache_program_lib_name} \"${cache_dev_source_file}\" ${app_dev_build_dir} ${program_lib_include_dir} ${program_user_lib}
)
add_custom_target(
        dpacc_${cache_sample_name}_target ALL
        DEPENDS dpacc_${cache_sample_name}
)
add_dependencies(${cache_sample_name} dpacc_${cache_sample_name}_target)
target_link_libraries(${cache_sample_name} ${LIBRARIES} ${app_dev_build_dir}/${cache_program_lib_name}.a ibverbs mlx5)
