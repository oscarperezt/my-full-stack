import {
  Button,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import { type ApiError, type DeviceCreate, DevicesService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

interface AddDeviceProps {
  isOpen: boolean
  onClose: () => void
}

const AddDevice = ({ isOpen, onClose }: AddDeviceProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<DeviceCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      device_name: "",
      description: "",
      provider_device_id: "",
      is_online: false,
      last_online_timestamp: null,
      last_reported_latitude: null, // Hidden field, set to null
      last_reported_longitude: null, // Hidden field, set to null
    },
  })

  const mutation = useMutation({
    mutationFn: (data: DeviceCreate) =>
      DevicesService.createDevice({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "Device created successfully.", "success")
      reset()
      onClose()
    },
    onError: (err: ApiError) => {
      handleError(err, showToast)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["devices"] })
    },
  })

  const onSubmit: SubmitHandler<DeviceCreate> = (data) => {
    mutation.mutate(data)
  }

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <ModalOverlay />
        <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
          <ModalHeader>Add Device</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <FormControl isRequired isInvalid={!!errors.device_name}>
              <FormLabel htmlFor="title">Name</FormLabel>
              <Input
                id="title"
                {...register("device_name", {
                  required: "Device name is required.",
                })}
                placeholder="Name"
                type="text"
              />
              {errors.device_name && (
                <FormErrorMessage>{errors.device_name.message}</FormErrorMessage>
              )}
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="description">Description</FormLabel>
              <Input
                id="description"
                {...register("description")}
                placeholder="Description"
                type="text"
              />
            </FormControl>
            <FormControl mt={4}>
              <FormLabel htmlFor="provider_device_id">Provider Device ID</FormLabel>
              <Input
                id="provider_device_id"
                {...register("provider_device_id")}
                placeholder="Provider Device ID"
                type="text"
              />
            </FormControl>
          </ModalBody>

          <ModalFooter gap={3}>
            <Button variant="primary" type="submit" isLoading={isSubmitting}>
              Save
            </Button>
            <Button onClick={onClose}>Cancel</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  )
}

export default AddDevice
