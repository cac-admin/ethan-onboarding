import Link from 'next/link';
import  {Box, Card, Stack, Typography, Button, CardOverflow, AspectRatio} from '@mui/joy';
import Image from 'next/image';
import Layout from '../components/layout';

export default function HomePage() {
    return(
        <Layout title="Queen's University Accessible Maps" description="An Accessible Map and Campus Access platform for Queen's University.">
            <Stack alignItems={'center'} justifyContent={'center'}>
                <Stack spacing={2} justifyContent={'center'}>
                    <AspectRatio ratio={"4/3"}>
                        <Image src="/images/Queens_University_logo.png" width={300} height={300} alt="Queen's University Logo"/>
                    </AspectRatio>
                    <Typography level="h1">Accessible Maps</Typography>

                    <Link href="/map/main"><Button variant="solid" sx={{width: "100%"}}>View Main Campus</Button></Link>
                    <Link href="/map/west"><Button variant="solid" sx={{width: "100%"}}>View West Campus</Button></Link>
                </Stack>
            </Stack>
        </Layout>
    );
}