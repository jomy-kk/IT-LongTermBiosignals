# -*- encoding: utf-8 -*-

# ===================================

# IT - PreEpiSeizures

# Package: pipeline
# File: Pipeline
# Description: Class representing a pipeline of steps that works on biosignals.

# Contributors: João Saraiva
# Created: 11/06/2022

# ===================================
from inspect import signature
from typing import List, Collection

from src.pipeline.Packet import Packet
from src.biosignals.Biosignal import Biosignal
from src.pipeline.PipelineUnit import PipelineUnit


class Pipeline():

    # Attributes
    __steps: List[PipelineUnit]
    __current_step: int
    __biosignals: Collection[Biosignal]
    __current_packet: Packet

    def __init__(self, name:str=None):
        self.name = name
        self.__current_step = 0
        self.__steps = []

    @property
    def current_step(self) -> int:
         if self.__current_step > 0:
             return self.__current_step
         else:
             raise AttributeError('Pipeline has not started yet.')

    @property
    def current_packet(self) -> Packet:
        return self.__current_packet

    def __len__(self):
        return len(self.__steps)

    def add(self, unit:PipelineUnit):
        if len(self) > 0:
            self.__check_completeness(unit)
        self.__steps.append(unit)

    def next(self):
        if self.__current_step == 0:  # if starting
            self.__create_first_packet()

        # Do next step
        self.__current_packet = self.__steps[self.__current_step]._apply(self.__current_packet)
        self.__current_step += 1

        if self.__current_step == len(self) - 1:  # if ending
            return self.__current_packet

    def applyAll(self):
        N_STEPS = len(self)
        while self.__current_step < N_STEPS:
            self.next()

    def __create_first_packet(self):
        assert self.__biosignals is not None  # Check if Biosignals were loaded
        all_timeseries = {}
        for biosignal in self.__biosignals:
            timeseries = biosignal._to_dict()
            assert tuple(timeseries.keys()) not in all_timeseries  # Ensure there are no repeated keys
            all_timeseries.update(timeseries)
        self.__current_packet = Packet(timeseries=all_timeseries)

    def __check_completeness(self, new_unit:PipelineUnit):
        load_that_will_be_available = {}
        for unit in self.__steps:
            # Get output label and type  # FIXME: Currently assuming only 1 output for PipelineUnit(s)
            output_label = tuple(unit.PIPELINE_OUTPUT_LABELS.values())[0]
            output_type = signature(new_unit.apply).return_annotation
            load_that_will_be_available[output_label] = output_type  # If it's the case, it replaces type of same labels, as it should

        new_unit_parameters = tuple(signature(new_unit.apply).parameters.values())

        for parameter in new_unit_parameters:
            parameter_name = parameter.name
            parameter_type = parameter.annotation
            input_label = new_unit.PIPELINE_INPUT_LABELS[parameter_name]  # Map to the label in Packet

            if input_label in load_that_will_be_available:
                if parameter_type == load_that_will_be_available[input_label]:
                    continue
                else:
                    raise AssertionError('Input type, {}, of {} of the new unit does not match the output type, {}, of the last unit.'.format(
                            parameter_type, parameter_name, load_that_will_be_available[input_label]))
            else:
                raise AssertionError('{} input label of the new unit does not match to any output label of the last unit.'.format(
                        input_label))



