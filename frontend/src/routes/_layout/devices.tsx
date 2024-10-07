import {
  Button,
  Container,
  Flex,
  Heading,
  SkeletonText,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useEffect } from "react"
import { z } from "zod"

import { DevicesService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"
import AddDevice from "../../components/Devices/AddDevice"

const devicesSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/devices")({
  component: Devices,
  validateSearch: (search) => devicesSearchSchema.parse(search),
})

const PER_PAGE = 5

function getDevicesQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      DevicesService.readDevices({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["devices", { page }],
  }
}

function DevicesTable() {
  const queryClient = useQueryClient()
  const { page } = Route.useSearch()
  const navigate = useNavigate({ from: Route.fullPath })
  const setPage = (page: number) =>
    navigate({ search: (prev) => ({ ...prev, page }) })

  const {
    data: devices,
    isPending,
    isPlaceholderData,
  } = useQuery({
    ...getDevicesQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const hasNextPage = !isPlaceholderData && devices?.data.length === PER_PAGE
  const hasPreviousPage = page > 1

  useEffect(() => {
    if (hasNextPage) {
      queryClient.prefetchQuery(getDevicesQueryOptions({ page: page + 1 }))
    }
  }, [page, queryClient, hasNextPage])

  return (
    <>
      <TableContainer>
        <Table size={{ base: "sm", md: "md" }}>
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Name</Th>
              <Th>Actions</Th>
              <Th>Latitude</Th>
              <Th>Longitude</Th>
              <Th>Last report</Th>
              <Th>Description</Th>
              <Th>Owner ID</Th>
              <Th>Device ID (Provider)</Th>
            </Tr>
          </Thead>
          {isPending ? (
            <Tbody>
              <Tr>
                {new Array(4).fill(null).map((_, index) => (
                  <Td key={index}>
                    <SkeletonText noOfLines={1} paddingBlock="16px" />
                  </Td>
                ))}
              </Tr>
            </Tbody>
          ) : (
            <Tbody>
              {devices?.data.map((device) => (
                <Tr key={device.id} opacity={isPlaceholderData ? 0.5 : 1}>
                  <Td isTruncated maxWidth="100px">{device.id}</Td>
                  <Td isTruncated maxWidth="200px">
                    {device.device_name}
                  </Td>
                  <Td>
                    <ActionsMenu type={"Device"} value={device} />
                  </Td>
                  <Td>{device.last_reported_latitude}</Td>
                  <Td>{device.last_reported_longitude}</Td>
                  <Td>{device.last_online_timestamp}</Td>
                  <Td
                    color={!device.description ? "ui.dim" : "inherit"}
                    isTruncated
                    maxWidth="150px"
                  >
                    {device.description || "N/A"}
                  </Td>
                  <Td isTruncated maxWidth="100px">{device.owner_id}</Td>
                  <Td isTruncated maxWidth="200px">{device.provider_device_id}</Td>
                </Tr>
              ))}
            </Tbody>
          )}
        </Table>
      </TableContainer>
      <Flex
        gap={4}
        alignItems="center"
        mt={4}
        direction="row"
        justifyContent="flex-end"
      >
        <Button onClick={() => setPage(page - 1)} isDisabled={!hasPreviousPage}>
          Previous
        </Button>
        <span>Page {page}</span>
        <Button isDisabled={!hasNextPage} onClick={() => setPage(page + 1)}>
          Next
        </Button>
      </Flex>
    </>
  )
}

function Devices() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Devices Management
      </Heading>

      <Navbar type={"Device"} addModalAs={AddDevice} />
      <DevicesTable />
    </Container>
  )
}
