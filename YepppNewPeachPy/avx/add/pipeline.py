from peachpy.x86_64 import ADD, SUB, JB, JAE, JZ, \
    ALIGN, Loop, \
    GeneralPurposeRegister32, GeneralPurposeRegister64


def software_pipelined_loop(reg_n, batch_elements,
                            instruction_columns, instruction_offsets):
    # Check that we have an offset for each instruction column
    assert len(instruction_columns) == len(instruction_offsets)
    assert isinstance(reg_n, (GeneralPurposeRegister32, GeneralPurposeRegister64))

    max_instructions = max(map(len, instruction_columns))

    batch_epilog = Loop()
    batch_loop = Loop()
    batch_prolog = Loop()

    from peachpy.stream import active_stream

    SUB(reg_n, batch_elements)
    JB(batch_epilog.end)

    with batch_prolog:
        for i in range(max_instructions):
            for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
                if i >= instruction_offset:
                    active_stream.add_instruction(instruction_column[i - instruction_offset])

    SUB(reg_n, batch_elements)
    JB(batch_epilog.begin)

    ALIGN(16)
    with batch_loop:
        for i in range(max_instructions):
            for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
                active_stream.add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

        SUB(reg_n, batch_elements)
        JAE(batch_loop.begin)

    with batch_epilog:
        for i in range(max_instructions):
            for instruction_column, instruction_offset in zip(instruction_columns, instruction_offsets):
                if i < instruction_offset:
                    active_stream.add_instruction(instruction_column[(i - instruction_offset) % max_instructions])

    ADD(reg_n, batch_elements)
