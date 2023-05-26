import Layout from "../../../components/layout";
import { getBuildingData, getAllIds } from "../../../lib/getbuildings";
import { Button, Card, Typography, Stack } from "@mui/joy";
import Link from "next/link";
import dynamic from "next/dynamic";
import Carousel from "../../../components/carousel";

export default function Building({ coords, buildingData }) {
    const DynMap = dynamic(() => import('../../../components/map-window'), {ssr: false,});

    return (
        <Layout title={`${buildingData.name} - Queen's University Accessible Maps`} description="An Accessible Campus Map View for Queen's University.">
            <Stack direction={"column"} spacing={2}>           
                <Stack spacing={2} direction={"row"} justifyContent={"space-between"}>
                    <Typography level="h1">{buildingData.name}</Typography>
                    <Link href="/map/main"><Button variant="solid" sx={{width: 150, height: 70}}>Back</Button></Link>
                </Stack>

                <Stack direction="row-reverse" spacing={2}>
                    <DynMap popup={false} zoom={20} buildings={[buildingData]} centre={buildingData.coords}/>
                    <Stack direction={"column"} spacing={2} sx={{width:"50%"}}>
                        <Typography level="h2">{buildingData.addr}</Typography>
                        <Carousel images={buildingData.images} />
                        <Card variant="outlined" className="fixed-size-scroll-window-hide" sx={{maxHeight: 400, overflow: "scroll"}}>
                            {(buildingData.location != "") ? (<><Typography level="h3">Location</Typography><Typography>{buildingData.location}</Typography></>) : (<></>)}
                            {(buildingData.entrances != [] && buildingData.entrances != "") ? (<><Typography level="h3">Entrances</Typography>{buildingData.entrances.map((value) => (<Typography level="p" key={value}>{value}</Typography>))}</>) : (<></>)}
                            {(buildingData.corridors != "") ? (<><Typography level="h3">Corridors</Typography><Typography>{buildingData.corridors}</Typography></>) : (<></>)}
                            {(buildingData.wayfinding != "") ? (<><Typography level="h3">Wayfinding</Typography><Typography>{buildingData.wayfinding}</Typography></>) : (<></>)}
                            {(buildingData.washrooms != "") ? (<><Typography level="h3">Washrooms</Typography><Typography>{buildingData.washrooms}</Typography></>) : (<></>)}
                            {(buildingData.fountains != "") ? (<><Typography level="h3">Fountains</Typography><Typography>{buildingData.fountains}</Typography></>) : (<></>)}
                            {(buildingData.classrooms != "") ? (<><Typography level="h3">Classrooms</Typography><Typography>{buildingData.classrooms}</Typography></>) : (<></>)}
                            {(buildingData.elevators != "") ? (<><Typography level="h3">Elevators</Typography><Typography>{buildingData.elevators}</Typography></>) : (<></>)}
                            {(buildingData.services != "") ? (<><Typography level="h3">Services</Typography><Typography>{buildingData.services}</Typography></>) : (<></>)}
                            {(buildingData.parking != "") ? (<><Typography level="h3">Parking</Typography><Typography>{buildingData.parking}</Typography></>) : (<></>)}
                            {(buildingData.access != [] && buildingData.access[0] != " " && buildingData.access != "") ? (<><Typography level="h3">Other</Typography>{buildingData.access.map((value) => (<Typography level="p" key={value}>{value}</Typography>))}</>) : (<></>)}
                        </Card>
                    </Stack>
                </Stack>
            </Stack>
        </Layout>
    )
  }

export async function getStaticPaths() {
    const paths = getAllIds();
    return {
        paths,
        fallback: false,
    }
}

export async function getStaticProps({ params }) {
    const buildingData = getBuildingData(params.id)
    return {
        props: {
            buildingData
        }
    }
}